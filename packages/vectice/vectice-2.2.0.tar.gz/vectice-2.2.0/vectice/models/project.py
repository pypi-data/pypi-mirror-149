from __future__ import annotations

import logging
from typing import Optional, List, TYPE_CHECKING, Union, Dict

from vectice.api import Page
from vectice.api.json import (
    JobType,
    ModelType,
    DatasetInput,
    DatasetVersionInput,
    ModelInput,
    JobInput,
    CodeVersionInput,
)
from .git_version import GitVersion
from .code_version import CodeVersion
from .data_resource import DataResource
from .dataset_metadata import DatasetMetadata
from .dataset import Dataset
from .integration import AbstractIntegration
from .job import Job
from .model import Model
from ..api.json.property import create_properties_input

if TYPE_CHECKING:
    from vectice import Reference
    from vectice.models import Workspace, Connection


class Project:
    """
    a project contains resources relative to a specific project.

    A project can contain :

    + documentation describing the project (goals, status, ...)
    + several datasets,
    + several models
    + several jobs

    A project can contains several datasets. Each datasets contains its own history.
    This is the same for models and jobs.

    :new_feature:
    """

    def __init__(
        self,
        id: int,
        workspace: Workspace,
        name: str,
        description: Optional[str] = None,
    ):
        """

        :param id: Project identifier
        :param workspace: the workspace reference this project belong to
        :param name: Name of the project
        :param description: Quick description of the project
        """
        self._id = id
        self._workspace = workspace
        self._name = name
        self._description = description
        self._client = workspace._client
        self._integration_client: Optional[AbstractIntegration] = workspace._integration_client

    def __repr__(self):
        return f"Project(name={self.name}, id={self.id}, description={self.description}, workspace={self.workspace})"

    def update(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> None:
        """
        Updates the information of the project.

        :new_feature:

        :param name: The name of the project.
        :param description: the description of the project

        :return: None
        """
        pass

    @property
    def id(self) -> int:
        """
        Project identifier
        :return:
        """
        return self._id

    @property
    def workspace(self) -> Workspace:
        """
        The workspace this project belong to
        :return:
        """
        return self._workspace

    @property
    def name(self) -> str:
        """
        Name of the project
        :return:
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        Quick description of the project
        :return:
        """
        return self._description

    def delete(self) -> None:
        """
        indicate if thecurrent project is deleted

        :new_feature:

        :return: None
        """
        pass

    def list_jobs(
        self,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> List[Job]:
        """
        List the jobs in this project

        The search parm helps filter the jobs depending on the name given.

        :param search: The name to search
        :param page_index: The page index
        :param page_size: The page size

        :return: List of Jobs
        """
        outputs = self._client.list_jobs(self.id, None, search, page_index, page_size)
        return [Job(item.name, item.id, self, item.description, item.type) for item in outputs.list]

    def delete_job(self, job: Reference) -> None:
        """
        Delete the specified job in the current project.

        :new_feature:

        :param job: The job name or id

        :return: None
        """
        self._client.delete_job(job, self.id)

    def get_job(self, job: Reference) -> Job:
        """
        Get a job.

        :since:3.0.0

        :param job: The job name or id
        :return: A Job or None if not found

        """
        item = self._client.get_job(job, self.id)
        return Job(item.name, item.id, self, item.description, item.type)

    def create_job(
        self,
        name: str,
        description: Optional[str] = None,
        type: JobType = JobType.OTHER,
    ) -> Job:
        """
        Create a new job in the project with the given attributes.

        The name is required and must be unique in the project.

        The default job type is `OTHER`. check the :class:`JobType` for other possible values.

        :param name: name of the job
        :param description: quick description of the job
        :param type: the type of the job

        :return: the newly created job
        """
        data = JobInput(name, description, type)
        output = self._client.create_job(data, self.id)
        return Job(output.name, output.id, self, output.description, output.type)

    def update_job(
        self,
        job: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[JobType] = None,
    ) -> Job:
        """
        Update the specified job with the new attribute values.

        :since:3.0.0

        :param job: The name or identifier of the job to update
        :param name: The name of the job
        :param type: The job type
        :param description: The description of the job

        :return: None
        """
        data = self._client.get_job(job, self.id)
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if type is not None:
            data["type"] = type
        output = self._client.update_job(data, self.id)
        return Job(output.name, output.id, self, output.description, output.type)

    def list_datasets(self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20) -> List[Dataset]:
        """
        List the datasets of this project

        The search param filter the datasets with the specified name.

        :param search: The model to search
        :param page_index:
        :param page_size:
        :return: List of Models
        """
        outputs = self._client.list_datasets(self.id, None, search, page_index, page_size)
        return [
            Dataset(
                item.name,
                item.id,
                self,
                item.description,
                Connection(
                    item.connection.id,
                    item.connection.name,
                    self.workspace,
                    item.connection.type,
                    item.connection.description,
                )
                if item.connection is not None
                else None,
            )
            for item in outputs.list
        ]

    def get_dataset(self, dataset: Reference) -> Dataset:
        """
        Get a dataset

        :param dataset: dataset name or id

        :return: A Dataset or None if not found
        """
        dataset_output = self._client.get_dataset(dataset, self.id, self.workspace.id)
        return Dataset(
            dataset_output.name,
            dataset_output.id,
            project=self,
            description=dataset_output.description,
        )

    def create_dataset(
        self,
        name: str,
        pattern: str = "*",
        description: Optional[str] = None,
        properties: Optional[Dict[str, Union[str, int, float]]] = None,
        connection: Optional[Reference] = None,
        resources: Optional[List[str]] = None,
    ) -> Dataset:
        """
        Create a new dataset in a specific project.

        :param name: The name of the dataset
        :param pattern: The dataset pattern
        :param description: The description of the dataset
        :param properties: The properties of the dataset version
        :param connection: The connection name or id the dataset belong to
        :param resources: The file/s of the dataset version

        :return: Dataset
        """
        data = DatasetInput(
            name=name,
            pattern=pattern,
            dataProperties=properties,
            description=description,
            connectionId=connection if isinstance(connection, int) else None,
            connectionName=connection if isinstance(connection, str) else None,
        )
        data_resources = DataResource.create_resources(resources)
        if data_resources is not None and len(data_resources) > 0:
            data["dataResources"] = data_resources
        dataset_output = self._client.create_dataset(data, self.id)
        if properties is not None:
            version_properties = create_properties_input(properties)
            version = DatasetVersionInput(properties=version_properties)
            self._client.create_dataset_version(version, dataset_output.id)
        logging.info(f"Dataset: {name} has been successfully created.")
        return Dataset(
            dataset_output.name,
            dataset_output.id,
            project=self,
            description=dataset_output.description,
        )

    def update_dataset(
        self,
        dataset: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        connection: Optional[Reference] = None,
        resources: Optional[List[str]] = None,
    ) -> Dataset:
        """
        Updates a dataset

        Updates a dataset. The connection is associated with the resources, e.g gcs connection for a gcs resource. If the updated resource requires a different connection
        then the connection must be updated. If the resource hash has not changed then the resource will not be updated. The resource could be linked to multiple versions
        of the dataset so ensure you want to update it, to avoid any unforeseen impacts to your experiment.

        :since:3.0.0

        :param dataset: dataset name or id
        :param name: The name of the dataset version e.g Changes 'Version 1' to 'name'
        :param description: The description of the dataset version
        :param connection: The connection name or id
        :param resources: The file/s of the dataset version

        :return: None
        """
        dataset_output = self._client.get_dataset(dataset, self.id, self.workspace.id)
        data_resources = DataResource.create_resources(resources)
        if data_resources is not None and len(data_resources) > 0:
            dataset_output["dataResources"] = data_resources
        if name is not None:
            dataset_output["name"] = name
        if description is not None:
            dataset_output["description"] = description
        if connection is not None:
            if isinstance(connection, int):
                dataset_output["connectionId"] = connection
            if isinstance(connection, str):
                dataset_output["connectionName"] = connection
        dataset_output = self._client.update_dataset(dataset_output, dataset, self.id, self.workspace.id)
        return Dataset(
            dataset_output.name,
            dataset_output.id,
            project=self,
            description=dataset_output.description,
            resources=data_resources,
        )

    def delete_dataset(self, dataset: Reference) -> None:
        """
        Delete the dataset with the specified reference.

        :new_feature:

        :param dataset: The dataset name or id

        :return: None
        """
        self._client.delete_dataset(dataset, self.id, self.workspace.id)

    def create_model(
        self,
        name: str,
        description: Optional[str] = None,
        type: Optional[ModelType] = ModelType.OTHER,
    ) -> Model:
        """
        Create a new model in the specified project.
        :param name: The name of the model
        :param description: The description of the model
        :param type: The model type e.g

        :return: A Model
        """
        data = ModelInput(name=name, description=description, type=type)
        model_output = self._client.create_model(data, self.id)
        return Model(model_output.name, model_output.id, self, model_output.description, ModelType[model_output.type])

    def update_model(
        self,
        model: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        type: Optional[ModelType] = ModelType.OTHER,
    ) -> Model:
        """
        Update a model with the new attribute values.

        :param model: the name or identifier of the model to update
        :param name: The name of the model
        :param description: The description of the model
        :param type: The model type

        :return: None
        """
        data = ModelInput(name=name, description=description, type=type)
        model_output = self._client.update_model(data, model, self.id)
        return Model(model_output.name, model_output.id, self, model_output.description, ModelType[model_output.type])

    def list_models(
        self, search: Optional[str] = None, page_index: int = Page.index, page_size: int = Page.size
    ) -> List[Model]:
        """
        List the models of the project

        The search param helps find the models with the specified name.

        :param search: The model to search
        :param page_index:
        :param page_size:

        :return: List of Models
        """
        outputs = self._client.list_models(self.id, None, search, page_index, page_size)
        return [Model(item.name, item.id, self, item.description, ModelType[item.type]) for item in outputs.list]

    def get_model(self, model: Reference) -> Model:
        """
        Get a model.

        Gets a model from the specified project.

        :since:3.0.0

        :param model: The model name or id
        :return: A Model or None if not found
        """
        model_output = self._client.get_model(model, self.id)
        return Model(model_output.name, model_output.id, self, model_output.description, ModelType[model_output.type])

    def delete_model(self, model: Reference) -> None:
        """
        Delete the model with the specified reference.

        :new_feature:

        :param model: The model name or id
        :return: None
        """
        self._client.delete_model(model, self.id)

    def create_code_version(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        uri: Optional[str] = None,
        is_starred: Optional[bool] = None,
        git_version: Optional[GitVersion] = None,
    ) -> CodeVersion:
        """
        Gets a specific version of this code.

        :param name: The version name or id
        :param description:
        :param uri:
        :param is_starred:
        :param is_starred:
        :param git_version:

        :return: A CodeVersion or None if the version does not exist
        """
        code_version_input = CodeVersionInput(
            name=name,
            description=description,
            uri=uri,
            is_starred=is_starred,
            gitVersion=git_version,
        )
        code_version_output = self._client.create_code_version(code_version_input, self.id)
        return CodeVersion(
            project=self,
            id=code_version_output.id,
            name=code_version_output.name,
            description=code_version_output.description,
            uri=code_version_output.uri,
            is_starred=code_version_output.is_starred,
            git_version=GitVersion(
                repositoryName=code_version_output.git_version.repository_name,
                branchName=code_version_output.git_version.branch_name,
                isDirty=code_version_output.git_version.is_dirty,
                commitHash=code_version_output.git_version.commit_hash,
                commitComment=code_version_output.git_version.commit_comment,
                entrypoint=code_version_output.git_version.entrypoint,
                commitAuthorName=code_version_output.git_version.commit_author_name,
                commitAuthorEmail=code_version_output.git_version.commit_author_email,
                uri=code_version_output.git_version.uri,
            )
            if code_version_output.git_version is not None
            else None,
            version=code_version_output.version,
            code_id=code_version_output.code_id,
        )

    def get_code_version(
        self,
        version: Reference,
    ) -> CodeVersion:
        """
        Gets a specific version of this code.

        :param version: The version name or id

        :return: A CodeVersion or None if the version does not exist
        """
        code_version_output = self._client.get_code_version(version, self.id)
        return CodeVersion(
            project=self,
            id=code_version_output.id,
            name=code_version_output.name,
            description=code_version_output.description,
            attachments="",
            is_starred=code_version_output.is_starred,
            version=code_version_output.version,
            git_version=GitVersion(**code_version_output.git_version.__dict__)
            if code_version_output.git_version is not None
            else None,
        )

    def list_code_versions(
        self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> List[CodeVersion]:
        """
        List the dataset versions.

        Returns a List of the Dataset Versions associated with the Dataset.
        The DatasetVersion can be used in runs or experiments.

        :param search: The name that contains the code versions
        :param page_index: The page index
        :param page_size: The page size

        :return: List of DatasetVersions
        """

        code_version_output_list = self._client.list_code_versions(self.id, None, search, page_index, page_size)
        return [
            CodeVersion(
                project=self,
                id=code_version_output.id,
                name=code_version_output.name,
                description=code_version_output.description,
                is_starred=code_version_output.is_starred,
                git_version_id=code_version_output.git_version_id,
                version=code_version_output.version,
            )
            for code_version_output in code_version_output_list
        ]

    def update_code_version(
        self,
        version: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_starred: Optional[bool] = None,
        uri: Optional[str] = None,
        git_version: Optional[GitVersion] = None,
    ) -> CodeVersion:
        """
        Update a code version.

        :since:3.0.0

        :param version: The code version name or id
        :param name: The name of the code version e.g Changes 'Version 1' to 'name'
        :param description: The description of the code version
        :param is_starred: Whether the dataset version is starred
        :param uri:
        :return: The updated code version
        """

        code_version_object = self._client.get_code_version(version, self.id)
        if code_version_object is None:
            raise ValueError("The code version was not found. Please check the reference.")
        code_version_input = CodeVersionInput(
            name=name, description=description, isStarred=is_starred, uri=uri, GitVersion=git_version
        )

        code_version_output = self._client.update_code_version(code_version_input, code_version_object.id, self.id)
        return CodeVersion(
            project=self,
            id=code_version_output.id,
            name=code_version_output.name,
            description=code_version_output.description,
            is_starred=code_version_output.is_starred,
            version=code_version_output.version_number,
            git_version_id=code_version_output.git_version_id,
        )

    def delete_code_version(
        self,
        version: Reference,
    ) -> None:
        """
        Delete a specific version of this code.

        :new_feature:
        :param version: The code version name or id
        :return: None
        """
        self._client.delete_code_version(version, self.id)
