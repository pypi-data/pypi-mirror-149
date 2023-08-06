from __future__ import annotations

from datetime import datetime
from typing import Optional, Dict, List, Union, BinaryIO, Any

from vectice import Vectice
from vectice.api import BadReferenceError, Reference
from vectice.api.json import (
    JobArtifactType,
    ModelVersionStatus,
    RunStatus,
    JobType,
    AutoVersionStrategy,
    TreeItem,
)
from vectice.integrations import Integrations
from vectice.models import ArtifactReference
from vectice.models import CodeVersion
from vectice.models import DatasetVersion, Dataset
from vectice.models import ModelVersion, Model
from vectice.models import Run, DataResource


def _ensure_reference(item: Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]) -> ArtifactReference:
    if isinstance(item, ArtifactReference):
        return item
    elif isinstance(item, CodeVersion):
        return ArtifactReference(code=item.code_id, version_id=item.id)
    elif isinstance(item, ModelVersion):
        return ArtifactReference(model=item.model.id, version_id=item.id)
    elif isinstance(item, DatasetVersion):
        return ArtifactReference(dataset=item.dataset.id, version_id=item.id)
    else:
        raise RuntimeError(f"can not create artifact reference from unknown object '{item}'")


class Experiment:
    """
    High level API that manages adapter and low level client. Multiple models can belong to an Experiment.

    Manages a run and implicitly manages the dataset version, model version, code version etc of the run.

    The workflow follows: `tasks -> experiment.start() -> tasks -> experiment.complete() -> auxiliary tasks`

    As a consequence, we got by default:

    - Any Model/Dataset/Code **before** the call to :func:`~Experiment.start` is an input
    - Any Model/Dataset/Code **after** the call to :func:`~Experiment.start` is an output.

    Any Model/Dataset/Code can be assigned as an input or output if the use cases requires something beyond
    the generic workflow.


    :new_feature:

    """

    def __init__(
        self,
        job: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        user_token: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        lib: Optional[object] = None,
        auto_code: bool = False,
        allow_self_signed_certificate: bool = True,
        auto_log: bool = False,
        job_type: JobType = JobType.OTHER,
        check_remote_repository: bool = True,
    ):
        """
        :param user_token: The user token to access a Vectice organisation.
        :param workspace: The workspace name or id the user wants to access.
        :param project: The project name or id the user wants to access.
        :param job: The job the user wants to work with or create.
        :param job_type: The job type the user defines.
        """
        self.job = job
        self._vectice = Vectice(
            workspace,
            project,
            user_token,
            api_endpoint,
            lib,
            allow_self_signed_certificate,
            auto_log,
        )
        self._auto_code = auto_code
        self._check_remote_repository = check_remote_repository
        self._inputs: List[ArtifactReference] = []
        self._outputs: List[ArtifactReference] = []
        self._active_run: Optional[Run] = None
        try:
            self._job = self._vectice.get_job(job)
        except BadReferenceError:
            if isinstance(job, str):
                self._job = self._vectice.create_job(name=job, type=job_type)

    def __repr__(self):
        lib = self._vectice._integration_client
        return (
            "Experiment("
            + f"job={self._job.name}, "
            + f"project={self._job.project.name}, "
            + f"workspace={self._job.project.workspace.name}, "
            + f"auto_code={self._auto_code}, "
            + f"api_endpoint={self._vectice._client._auth.api_base_url}, "
            + f"lib={lib.lib_name() if lib is not None else 'None'})"
        )

    @property
    def vectice(self) -> Vectice:
        return self._vectice

    def _get_run(
        self,
        create_run: bool = False,
        auto_code: Optional[bool] = None,
        check_remote_repository: Optional[bool] = None,
        run_notes: Optional[str] = None,
        run_properties: Optional[Dict] = None,
        system_name: Optional[str] = None,
    ) -> Optional[Run]:
        if self._active_run is None and create_run:
            run = self._job.create_run(
                name=f"Run {datetime.now().isoformat()}",
                properties=run_properties,
                auto_code=auto_code if auto_code is not None else self._auto_code,
                check_remote_repository=check_remote_repository
                if check_remote_repository is not None
                else self._check_remote_repository,
                notes=run_notes,
                system_name=system_name,
            )
            self._active_run = run
        return self._active_run

    def _add_artifact_reference(
        self, artifact_reference: ArtifactReference, artifact_type: Optional[JobArtifactType] = None
    ):
        run = self._get_run(create_run=False)
        if run is None:
            if self._is_input(artifact_type):
                self._inputs.append(artifact_reference)
            else:
                self._outputs.append(artifact_reference)
        else:
            if self._is_input(artifact_type):
                run.add_input(artifact_reference)
            else:
                run.add_output(artifact_reference)

    def use_dataset_version(
        self,
        dataset: Reference,
        version_name: Optional[str] = None,
        version_number: Optional[int] = None,
        version_id: Optional[int] = None,
        version_strategy: Optional[AutoVersionStrategy] = None,
        artifact_type: Optional[JobArtifactType] = None,
    ) -> ArtifactReference:
        result = None
        # check priorities
        # id > name > number > strategy
        if version_id is not None:
            result = ArtifactReference(dataset=dataset, version_id=version_id)
        elif version_name is not None:
            result = ArtifactReference(dataset=dataset, version_name=version_name)
        elif version_number is not None:
            result = ArtifactReference(dataset=dataset, version_number=version_number)
        elif version_strategy is not None:
            result = ArtifactReference(dataset=dataset, version_strategy=version_strategy)
        else:
            raise RuntimeError(
                "missing information to find the version of the dataset. You need to give one of the version identification"
            )
        self._add_artifact_reference(result, artifact_type)
        return result

    def add_dataset_version(
        self,
        dataset: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_starred: Optional[bool] = None,
        properties: Optional[Dict[str, Any]] = None,
        resources: Optional[List[str]] = None,
        metadata: Optional[Union[str, List[str]]] = None,
        artifact_type: Optional[JobArtifactType] = None,
        attachment: Optional[Union[str, List[str]]] = None,
    ) -> DatasetVersion:
        """
        Adds a Dataset Version to the managed run.

        If the Dataset Version exists already then the existing Dataset Version is used. If the Dataset Version
        does not exist then the Dataset Version will be created and added to the managed run. The Dataset Version
        can be passed as an input or output; if it isn't then the workflow process is followed and added as
        an input or output. Resources are cloud provider assets e.g Google Cloud Storage with a connection in the
        Vectice UI and metadata are assets with no connection in Vectice UI.

        :param dataset: The dataset name or id
        :param name: The name of the dataset version e.g Changes 'Version 1' to 'name'
        :param description: The description of the dataset version
        :param is_starred: Whether the dataset version is starred
        :param properties: The properties of the dataset version
        :param resources: The resource uri/s of the dataset version
        :param metadata: The metadata uri/s of the dataset version
        :param artifact_type: indicate if the dataset version is an input ou an output
        :param attachment: The attachment of the code version

        :since:3.0.0

        :return: None
        """
        project_id = self._vectice.project.id if self._vectice.project is not None else None
        workspace_id = self._vectice.workspace.id if self._vectice.workspace is not None else None
        dataset_version = self._vectice.create_dataset_version(
            dataset,
            name,
            project_id,
            workspace_id,
            description,
            is_starred,
            properties,
            resources,
            metadata,
            attachment,
        )
        self._add_artifact_reference(
            ArtifactReference(
                dataset=dataset,
                version_name=dataset_version.name,
                version_id=dataset_version.id,
            ),
            artifact_type,
        )
        return dataset_version

    def update_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_starred: Optional[bool] = None,
        properties: Optional[Dict[str, Any]] = None,
    ) -> DatasetVersion:
        """
        Update a dataset version.

        Updates the dataset version given by the user.

        :since:3.0.0

        :param dataset: dataset name or id
        :param dataset_version: The dataset version name or id
        :param name: The name of the dataset version e.g Changes 'Version 1' to 'name'
        :param description: The description of the dataset version
        :param is_starred: Whether the dataset version is starred
        :param properties: The properties of the dataset version

        :return: None
        """
        return self._vectice.update_dataset_version(
            version, dataset, None, None, name, description, is_starred, properties
        )

    def list_datasets(self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20) -> List[Dataset]:
        """
        List all the Datasets associated with the project.

        :param search: A search term
        :param page_index: The page index
        :param page_size: The page size

        :return: A list of Datasets
        """
        return self._vectice.list_datasets(search=search, page_index=page_index, page_size=page_size)

    def list_dataset_versions(
        self, dataset: Reference, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> List[DatasetVersion]:
        """
        List the dataset versions.

        Lists the dataset versions of the specified dataset.

        :param dataset: dataset name or id

        :return: List of DatasetVersions
        """
        project_ref = None
        workspace_ref = None
        return self._vectice.list_dataset_versions(dataset, project_ref, workspace_ref, search, page_index, page_size)

    def get_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
    ) -> Optional[DatasetVersion]:
        """
        Get a dataset version.

        Gets a specific dataset version of the specified dataset.

        :param dataset: dataset name or id
        :param dataset_version: The dataset version name or id

        :return: A DatasetVersion
        """
        return self._vectice.get_dataset_version(version, dataset)

    def delete_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
    ) -> None:
        """
        Delete a dataset version.

        Deletes a specific dataset in the specified project.

        :new_feature:

        :param dataset: dataset name or id
        :param dataset_version: The dataset version name or id

        :return: None
        """
        self._vectice.delete_dataset_version(version, dataset)

    def start(
        self,
        auto_code: Optional[bool] = None,
        check_remote_repository: Optional[bool] = None,
        run_notes: Optional[str] = None,
        run_properties: Optional[Dict] = None,
        system_name: Optional[str] = None,
        inputs: Optional[List[Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]]] = None,
    ) -> Run:
        """
        Start the current experiments run.

        Once the run has started, all the Dataset/Model/Code Versions
        will be captured as outputs of the run.

        The group name allow to group several runs in one global run

        :since:3.0.0

        :return: None
        """
        if inputs is not None:
            artifacts_references_inputs = [_ensure_reference(item) for item in inputs if item is not None]
            self._inputs.extend(artifacts_references_inputs)
        current_run = self._get_run(
            create_run=True,
            auto_code=auto_code,
            check_remote_repository=check_remote_repository,
            run_notes=run_notes,
            run_properties=run_properties,
            system_name=system_name,
        )
        if current_run is not None:
            for input in self._inputs:
                current_run.add_input(input)
            for output in self._outputs:
                current_run.add_output(output)
            current_run.start(auto_code=auto_code, check_remote_repository=check_remote_repository)
            return current_run
        else:
            raise RuntimeError("can not create run")

    def complete(
        self, outputs: Optional[List[Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]]] = None
    ) -> None:
        """
        Complete the current experiment run.

        Once the run is complete. All the Dataset/Model/Code Version/s will be captured as outputs to
        the run, that were done after the experiment.start().


        :since:3.0.0

        :param run_name: The run name the user defines.
        :param group_name: The group name the user defines.
        :param datasets: The Dataset(s) to be used as inputs of the run
        :param models: The Model(s) to be used as inputs of the run
        :param dataset_versions: The Dataset Version(s) to be used as inputs of the run
        :param model_versions: The Model Version(s) to be used as inputs of the run

        :return: None
        """
        current_run = self._get_run(create_run=False)
        if current_run is not None:
            if outputs is not None:
                artifacts_references_outputs = [_ensure_reference(item) for item in outputs if item is not None]
                current_run.add_outputs(artifacts_references_outputs)
            current_run.complete()
        self._active_run = None
        self._inputs = []
        self._outputs = []

    def fail(
        self,
        reason: Optional[str] = None,
        outputs: Optional[List[Union[ArtifactReference, CodeVersion, ModelVersion, DatasetVersion]]] = None,
    ) -> None:
        """
        Fail the current experiment run.

        Marks the experiment run as failed. Which will appear as the runs' STATUS, this can be viewed
        in the Vectice UI.


        :since:3.0.0

        :param reason: indicate why the run failed

        :return: None
        """
        current_run = self._get_run(create_run=False)
        if current_run is not None:
            if outputs is not None:
                artifacts_references_outputs = [_ensure_reference(item) for item in outputs if item is not None]
                current_run.add_outputs(artifacts_references_outputs)
            current_run.fail(reason=reason)
        self._active_run = None

    def abort(self, reason: Optional[str] = None) -> None:
        """
        Abort the current experiment run.

        Marks the experiment run as aborted. Which will appear as the runs' STATUS, this can be viewed
        in the Vectice UI.


        :since:3.0.0

        :param reason: Indicates why the run was aborted

        :return: None
        """
        current_run = self._get_run(create_run=False)
        if current_run is not None:
            current_run.abort(reason=reason)
        self._active_run = None

    def add_model_version_attachment(
        self,
        file: str,
        model_version: Reference,
        model: Optional[Reference] = None,
    ) -> None:
        """
        attach a file to an existing Model Version.

        The Model Version Attachment will be added and associated to the Model Version if it exists.
        The Attachment is directly uploaded to Vectice and can be viewed immediately if the operation
        is successful. The Attachment can be seen in the Vectice UI or interacted with with the Python SDK.


        :since:3.0.0

        :param file: A file to attach on the model version
        :param model: The model name or id
        :param model_version: The model version name or id

        :return: None
        """
        self._vectice.add_model_version_attachment(file, model_version, model)

    def delete_model_version_attachment(
        self,
        file: str,
        model_version: Reference,
        model: Optional[Reference] = None,
    ) -> None:
        """
        Delete a Model Version Attachment.

        Deletes the specified attachment from the model version.


        :since:3.0.0

        :param model: The model name or id
        :param model_version: The model version name or id
        :param file: The file name

        :return: None
        """
        self._vectice.delete_model_version_attachment(file, model_version, model)

    def get_model_version_attachment(
        self,
        file: str,
        model_version: Reference,
        model: Optional[Reference] = None,
    ) -> Optional[BinaryIO]:
        """
        Get a model version attachment.

        Gets the attachment of a model version.

        :param model: The model name or id
        :param model_version: The model version name or id
        :param file: The file name

        :return: An Artifact Version Attachment
        """
        return self._vectice.get_model_version_attachment(file, model_version, model)

    def list_models(self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20) -> List[Model]:
        """
        List all the Models associated with the project.

        :param search: A search term
        :param page_index: The page index
        :param page_size: The page size

        :return: A list of Models
        """
        return self._vectice.list_models(search=search, page_index=page_index, page_size=page_size)

    def list_model_version_attachments(
        self,
        model_version: Reference,
        model: Optional[Reference] = None,
    ) -> List[str]:
        """
        List the files attached to a Model version.

        :param model: The model name or id
        :param model_version: The model version name or id

        :return: A list of file names
        """
        return self._vectice.list_model_version_attachments(model_version, model)

    def add_dataset_version_attachment(
        self,
        file: str,
        dataset_version: Reference,
        dataset: Optional[Reference] = None,
    ) -> None:
        """
        Adds a Dataset Version Attachment to an existing Dataset Version.

        The Dataset Version Attachment will be added and associated to the Dataset Version if it exists.
        The Attachment is directly uploaded to Vectice and can be viewed immediately if the operation
        is successful. The Attachment can be seen in the Vectice UI or interacted with with the Python SDK.


        :new_feature:

        :param file: A file to attach on the dataset version
        :param dataset: The dataset name or id
        :param dataset_version: The dataset version name or id

        :return: None
        """
        self._vectice.add_dataset_version_attachment(file, dataset_version, dataset)

    def delete_dataset_version_attachment(
        self,
        file: str,
        dataset_version: Reference,
        dataset: Optional[Reference] = None,
    ) -> None:
        """
        Delete a Dataset Version Attachment.

        Deletes the specified attachment from the dataset version.


        :since:3.0.0

        :param dataset: The dataset name or id
        :param dataset_version: The dataset version name or id
        :param file: The file name

        :return: None
        """
        self._vectice.delete_dataset_version_attachment(file, dataset_version, dataset)

    def list_dataset_version_attachments(
        self,
        dataset_version: Reference,
        dataset: Optional[Reference] = None,
    ) -> List[str]:
        """
        List the files attached to a Dataset version.

        :param dataset: The dataset name or id
        :param dataset_version: The dataset version name or id

        :return: An Artifact Version Attachment
        """
        return self._vectice.list_dataset_version_attachments(dataset_version, dataset)

    def add_code_version_attachment(
        self,
        file: str,
        code_version: Reference,
    ) -> None:
        """
        Adds a Code Version Attachment to an existing Code Version.

        The Code Version Attachment will be added and associated to the Code Version if it exists.
        The Attachment is directly uploaded to Vectice and can be viewed immediately if the operation
        is successful. The Attachment can be seen in the Vectice UI or interacted with with the Python SDK.


        :new_feature:

        :param file: A file to attach on the dataset version
        :param code_version: The code version name or id

        :return: None
        """
        self._vectice.add_code_version_attachment(file, code_version)

    def delete_code_version_attachment(
        self,
        file: str,
        code_version: Reference,
    ) -> None:
        """
        Delete a Code Version Attachment.

        Deletes the specified attachment from the code version.

        :new_feature:

        :param code_version: The code version name or id
        :param file: The file name

        :return: None
        """
        self._vectice.delete_code_version_attachment(file, code_version)

    def get_code_version_attachment(
        self,
        file: str,
        code_version: Reference,
    ) -> Optional[BinaryIO]:
        """
        Get a code version attachment.

        Gets the attachment of a code version.

        :new_feature:

        :param code_version: The code version name or id
        :param file: The file name

        :return: A list of file name or uri
        """
        return self._vectice.get_code_version_attachment(file, code_version)

    def list_code_version_attachments(
        self,
        code_version: Reference,
    ) -> List[str]:
        """
        List the files attached to a Code version.

        :new_feature:

        :param code_version: The code version name or id
        :return: A list of file name or uri
        """
        return self._vectice.list_code_version_attachments(code_version)

    def add_run_attachment(
        self,
        file: str,
        run: Reference,
        job: Optional[Reference] = None,
    ) -> None:
        """
        Adds a Code Version Attachment to an existing Code Version.

        The Code Version Attachment will be added and associated to the Code Version if it exists.
        The Attachment is directly uploaded to Vectice and can be viewed immediately if the operation
        is successful. The Attachment can be seen in the Vectice UI or interacted with with the Python SDK.


        :new_feature:

        :param file: A file to attach on the dataset version
        :param run: The run name or id
        :param job: The job name or id
        :return: None
        """
        return self._vectice.add_run_attachment(file, run, job)

    def delete_run_attachment(
        self,
        file: str,
        run: Reference,
        job: Optional[Reference] = None,
    ) -> None:
        """
        Delete a Code Version Attachment.

        Deletes the specified attachment from the code version.

        :new_feature:

        :param run: The run name or id
        :param job: The job name or id
        :param file: The file name

        :return: None
        """
        self._vectice.delete_run_attachment(file, run, job)

    def get_run_attachment(
        self,
        file: str,
        run: Reference,
        job: Optional[Reference] = None,
    ) -> Optional[BinaryIO]:
        """
        Get a code version attachment.

        Gets the attachment of a code version.

        :new_feature:

        :param run: The run name or id
        :param job: The job name or id
        :param file: The file name

        :return: A list of file name or uri
        """
        return self._vectice.get_run_attachment(file, run, job)

    def list_run_attachments(
        self,
        run: Reference,
        job: Optional[Reference] = None,
    ) -> List[str]:
        """
        List the files attached to a Code version.

        :new_feature:

        :param run: The run name or id
        :param job: The job name or id
        :return: A list of file name or uri
        """
        return self._vectice.list_run_attachments(run, job)

    def _is_input(self, artifact_type: Optional[JobArtifactType] = None) -> bool:
        if artifact_type == JobArtifactType.INPUT:
            return True
        elif artifact_type == JobArtifactType.OUTPUT:
            return False
        else:
            run = self._get_run(create_run=False)
            if run is None:
                return True
            else:
                return run.status == RunStatus.SCHEDULED

    def use_model_version(
        self,
        model: Reference,
        version_name: Optional[str] = None,
        version_number: Optional[int] = None,
        version_id: Optional[int] = None,
        artifact_type: Optional[JobArtifactType] = None,
    ) -> ArtifactReference:
        """
        Use an existing Model Version in the run as an input or output.

        If the Model Version exists. The Model Version can be used as an input or output; if it isn't then
        the workflow process is followed and if Model Version is an input or output,
        is identified in the workflow process.


        :since:3.0.0

        :param model: The model name or id the version belongs to
        :param version_name: The model version name
        :param version_id: The model version id
        :param version_number: The model version number
        :param artifact_type: indicate if the model version is an input ou an output

        :return: None
        """
        result = None
        if version_id is not None:
            result = ArtifactReference(model=model, version_id=version_id)
        elif version_name is not None:
            result = ArtifactReference(model=model, version_name=version_name)
        elif version_number is not None:
            result = ArtifactReference(model=model, version_number=version_number)
        else:
            raise RuntimeError(
                "missing information to find the version of the model. you need to give one of the version identification"
            )
        self._add_artifact_reference(result, artifact_type)
        return result

    def add_model_version(
        self,
        model: Reference,
        name: Optional[str] = None,
        algorithm: Optional[str] = None,
        status: ModelVersionStatus = ModelVersionStatus.EXPERIMENTATION,
        hyper_parameters: Optional[Dict] = None,
        metrics: Optional[Dict] = None,
        artifact_type: Optional[JobArtifactType] = None,
        attachment: Optional[Union[str, List[str]]] = None,
    ):
        """
        Adds a Model Version to the managed run.

        If the Model Version exists already then the existing Model Version is used. If the Model Version
        does not exist then the Model Version will be created and added to the managed run. The Model Version
        can be passed as an input or output; if it isn't then the workflow process is followed and added as
        an input or output.


        :since:3.0.0

        :param model: The model reference (model name or model id)
        :param name: The name of the model version
        :param algorithm: The models' algorithm
        :param status: The model status 'EXPERIMENTATION'/'STAGING'/'PRODUCTION'
        :param hyper_parameters: The hyper parameters of the model
        :param metrics: The metrics of the model
        :param artifact_type: indicate if the model version is an input ou an output
        :param attachment: The attachment of the code version

        :return: None
        """
        parent_model = self._vectice.get_model(model)
        model_version = parent_model.create_model_version(
            name, status=status, algorithm_name=algorithm, metrics=metrics, hyper_parameters=hyper_parameters
        )
        if attachment:
            model_version.add_attachments(attachment)
        self.use_model_version(model=model, version_id=model_version.id, artifact_type=artifact_type)

    def update_model_version(
        self,
        version: Reference,
        model: Optional[Reference] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[ModelVersionStatus] = ModelVersionStatus.EXPERIMENTATION,
        algorithm: Optional[str] = None,
        is_starred: Optional[bool] = False,
        metrics: Optional[Dict] = None,
        hyper_parameters: Optional[Dict] = None,
    ) -> ModelVersion:
        """
        Update a Model Version to the managed run.

        Updates the specified model version with the new params passed to this function.

        :param model: The model name or id the version belongs to
        :param version: The model version name or id
        :param name: The name of the model
        :param description: The description of the model
        :param status: The status of the model e.g 'EXPERIMENTATION'/'STAGING'/'PRODUCTION'
        :param algorithm: The algorithm the model version uses
        :param is_starred: Whether the model is starred or not
        :param metrics: The model version metrics
        :param hyper_parameters: The model version hyper parameters

        :return: None
        """
        return self._vectice.update_model_version(
            version, model, None, None, name, description, status, algorithm, is_starred, metrics, hyper_parameters
        )

    def list_model_versions(
        self, model: Reference, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> List[ModelVersion]:
        """
        List the model versions of a model.

        Lists all the versions created out of the specified model.

        :param model: The model name or id the versions belongs to

        :return: List of ModelVersions
        """
        return self._vectice.list_model_versions(model, search=search, page_index=page_index, page_size=page_size)

    def list_model_versions_dataframe(
        self, model: Reference, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> "pandas.DataFrame":  # type: ignore # noqa F821
        return self._vectice.list_model_versions_dataframe(
            model, search=search, page_index=page_index, page_size=page_size
        )

    def get_model_version(
        self,
        version: Reference,
        model: Optional[Reference] = None,
    ) -> ModelVersion:
        """
        Get a model version.

        Gets a specific version of a model.

        :since:3.0.0

        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id

        :return: A ModelVersion
        """
        return self._vectice.get_model_version(version, model)

    def delete_model_version(
        self,
        version: Reference,
        model: Optional[Reference] = None,
    ) -> None:
        """
        Delete a model version.

        Deletes the specified version of a model.

        :new_feature:

        :param model: The model name or id the version belongs to
        :param version: The model version name or id

        :return: None
        """
        self._vectice.delete_model_version(version, model)

    def add_code_version(
        self,
        git_path: str = ".",
        check_remote_repository: bool = True,
        attachments: Optional[Union[str, List[str]]] = None,
    ) -> Optional[CodeVersion]:
        """
        Adds a Code Version to the managed run.

        Creates a code version in the specified project using the git repository path of the code version.

        :param git_path: The path to the git repository
        :param check_remote_repository: Indicate if we check file existence in remote repository
        :param attachments: Resources to attach to the code version e.g AWS S3 or local files

        :return: A CodeVersion
        """
        code_version = self._vectice.create_code_version(
            uri=git_path, check_remote_repository=check_remote_repository, attachments=attachments
        )
        if code_version is not None:
            self._add_artifact_reference(ArtifactReference(code=code_version.code_id, version_id=code_version.id))
        return code_version

    def add_code_version_uri(
        self,
        git_uri: str,
        entrypoint: Optional[str] = None,
        artifact_type: Optional[JobArtifactType] = None,
        login_or_token: Optional[str] = None,
        password: Optional[str] = None,
        oauth2_token: Optional[str] = None,
        attachment: Optional[Union[str, List[str]]] = None,
    ) -> Optional[CodeVersion]:
        """
        Adds a Code Version to the managed run.

        If the Code Version exists already then the existing Code Version is used. If the Code Version
        does not exist then the Code Version will be created and added to the managed run. The Code Version
        can be passed as an input or output; if it isn't then the workflow process is followed and added as
        an input or output.


        :since:3.0.0

        :param git_uri: The uri of the file or folder in github/bitbucket/gitlab
        :param entrypoint: The relative path of the file or folder e.g folder/file.py
        :param artifact_type: indicate if the code version is an input ou an output
        :param login_or_token: A real login or a personal access token
        :param password: The password
        :param oauth2_token: The OAuth2 access token
        :param attachment: The attachment of the code version

        :return: None
        """

        git_version = Integrations.create_code_version_with_uri(
            git_uri, entrypoint, login_or_token, password, oauth2_token
        )
        if git_version is None:
            return None
        code_version = self._vectice.create_code_version(
            uri=git_version.uri, project=self._job.project.id, git_version=git_version
        )
        if isinstance(attachment, List):
            for item in attachment:
                if item is not None:
                    code_version.add_attachment(item)
        else:
            if attachment is not None:
                code_version.add_attachment(attachment)
        self._add_artifact_reference(ArtifactReference(code=code_version.code_id, version_id=code_version.id))
        return code_version

    def update_code_version(
        self,
        code_version: Reference,
        repository_name: str,
        branch_name: str,
        commit_hash: str,
        commit_comment: str,
        commit_author_name: str,
        commit_author_email: str,
        is_dirty: bool,
        uri: str,
        entrypoint: Optional[str] = None,
    ) -> None:
        """
        Update a code version.

        Updates the specified code version with the new given information in the params.

        :new_feature:

        :param code_version: The code version name or id
        :param repository_name: The repository name
        :param branch_name: The branch name
        :param commit_hash: The commit hash
        :param commit_comment: The commit comment
        :param commit_author_name: The commit author name
        :param commit_author_email: The commit author email
        :param is_dirty: Whether the commit is dirty
        :param uri: The uri
        :param entrypoint: The entrypoint

        :return: None
        """
        self._vectice.update_code_version(
            code_version,
            repository_name,
            branch_name,
            commit_hash=commit_hash,
            commit_comment=commit_comment,
            commit_author_name=commit_author_name,
            commit_author_email=commit_author_email,
            is_dirty=is_dirty,
            uri=uri,
            entrypoint=entrypoint,
        )

    def get_code_version(
        self,
        code_version: Reference,
    ) -> Optional[CodeVersion]:
        """
        Get a code version.

        Gets the specified version of a code artifact.

        :new_feature:

        :param code_version: The code version name or id

        :return: A CodeVersion
        """
        return self._vectice.get_code_version(code_version)

    def list_code_versions(
        self, code_version: Reference, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> Optional[List[CodeVersion]]:
        """
        List the code versions.

        Lists all the versions of a code artifact.

        :new_feature:

        :param code_version: The code version name or id

        :return: A List of CodeVersions
        """
        return self._vectice.list_code_versions(code_version, search=search, page_index=page_index, page_size=page_size)

    def delete_code_version(
        self,
        code_version: Reference,
    ) -> None:
        """
        Delete a code version.

        Deletes the specified version of a code artifact.

        :new_feature:

        :param code_version: The code version name or id

        :return: None
        """
        self._vectice.delete_code_version(code_version)

    def log_metric(
        self,
        model_version: Reference,
        key: str,
        value: int,
        model: Optional[Reference] = None,
        step: Optional[int] = None,
        epoch: Optional[int] = None,
    ) -> None:
        """
        Logs a metric to the Model Version specified.

        If the Model Version is not found the operation will fail. If the Model Version is found in the input or outputs
        the metrics will be directly uploaded to Vectice and assigned to the Model Version.
        A key is the metric name and the value is the metric value. Step and epoch are for deep learning models metrics.


        :param model: The model name or id
        :param model_version: The model version name or id/number
        :param key: The metric key
        :param value: The metric value
        :param step: The metric step
        :param epoch: The metric epoch

        :return: None
        """
        self._vectice.get_model_version(model_version, model).create_metrics(metrics={key: value})

    def log_metrics(
        self,
        model_version: Reference,
        metrics: Dict,
        model: Optional[Reference] = None,
        step: Optional[int] = None,
        epoch: Optional[int] = None,
    ) -> None:
        """
        Logs a dictionary of metrics to the Model Version specified.

        If the Model Version is not found the operation will fail. If the Model Version is found in the input or outputs
        the metrics will be directly uploaded to Vectice and assigned to the Model Version. A dictionary with the key,
        value, epoch and step is accepted.


        :param model: The model name or id
        :param model_version: The model version name or id/number
        :param metrics: A dictionary of metrics
        :param step: The metric step
        :param epoch: The metric epoch
        :return: None
        """
        self._vectice.get_model_version(model_version, model).create_metrics(metrics=metrics)

    def list_metrics(
        self,
        model_version: Reference,
        model: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> Optional[Dict[str, Any]]:
        """
        List the model version metrics.

        Lists the metrics used for the specified model version.

        :since:3.0.0

        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id
        :param search:
        :param page_index:
        :param page_size:

        :return: A List of Metrics
        """
        return self._vectice.get_model_version(model_version, model).list_metrics(
            search=search, page_index=page_index, page_size=page_size
        )

    def delete_metrics(
        self,
        model_version: Reference,
        metrics: List[str],
        model: Optional[Reference] = None,
    ) -> None:
        """
        Delete a model version metric.

        Deletes a metric used for the specified model version.

        :new_feature:

        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id
        :param metrics: The metric keys to delete

        :return: None
        """
        self._vectice.delete_model_version_metrics(model_version, metrics, model)

    def log_hyper_parameter(
        self,
        model_version: Reference,
        key: str,
        value: Union[int, float, str],
        model: Optional[Reference] = None,
    ) -> None:
        """
        Logs a hyper parameter to the Model Version specified.

        If the Model Version is not found the operation will fail. If the Model Version is found in the input or outputs
        the hyper parameter will be directly uploaded to Vectice and assigned to the Model Version.
        A key is the hyper parameter name and the value is the metric value.


        :param model: The model name or id
        :param model_version: The model version name or id/number
        :param key: The hyper parameter key
        :param value: The hyper parameter value

        :return: None
        """
        self._vectice.get_model_version(model_version, model).create_hyper_parameters(hyper_parameters={key: value})

    def log_hyper_parameters(
        self,
        model_version: Reference,
        hyper_parameters: Dict,
        model: Optional[Reference] = None,
    ) -> None:
        """
        Update a model version hyper parameters.

        If the Model Version is not found the operation will fail. If the Model Version is found in the input or outputs
        the metrics will be directly uploaded to Vectice and assigned to the Model Version. A dictionary with multiple
        key and value pairs is accepted.

        :since:3.0.0

        :param hyper_parameters: The hyper_parameter ids or keys
        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id

        :return: None
        """
        self._vectice.get_model_version(model_version, model).create_hyper_parameters(hyper_parameters=hyper_parameters)

    def list_hyper_parameters(
        self,
        model_version: Reference,
        model: Optional[Reference] = None,
    ) -> Dict:
        """
        List the model version hyper parameters.

        :since:3.0.0

        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id

        :return: A map containing the hyper parameters
        """
        return self._vectice.get_model_version(model_version, model).list_hyper_parameters()

    def delete_hyper_parameters(
        self,
        model_version: Reference,
        keys: List[str],
        model: Optional[Reference] = None,
    ) -> None:
        """
        Delete the model version hyper parameters

        Deletes the hyper parameters used for the specified model.

        :new_feature:

        :param keys: The list of keys to delete
        :param model: The model name or id the version belongs to
        :param model_version: The model version name or id

        :return: None
        """
        self._vectice.delete_model_version_hyper_parameters(model_version, keys, model)
