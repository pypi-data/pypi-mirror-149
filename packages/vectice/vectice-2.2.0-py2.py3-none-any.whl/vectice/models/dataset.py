from __future__ import annotations

import logging
from typing import Optional, Dict, List, Union, TYPE_CHECKING, Any

from vectice.api import Client
from vectice.api.json import DatasetVersionInput
from vectice.api.reference import InvalidReferenceError
from vectice.models import DatasetVersion, DataResource
from vectice.models.dataset_metadata import DatasetMetadata

if TYPE_CHECKING:
    from vectice import Reference
    from vectice.models import Project, Connection


class Dataset:
    """
    Describe a dataset

    There is several type of dataset:

    - dataset based on a Connection.
    - dataset without any Connection where we store only metadata
    - dataset without any Connection where we store local files and the associated metadata

    For dataset based on a Connection, The platform store metadata of the current state of the shared dataset.
    The SDK does not manage the metadata.

    For dataset without any Connection, the SDK calculate the metadata from the current state of the dataset.


    """

    def __init__(
        self,
        name: str,
        id: int,
        project: Project,
        description: Optional[str] = None,
        connection: Optional[Connection] = None,
        pattern: Optional[str] = "*",
        resources: Optional[List[str]] = None,
    ):
        """
        :param id: the project identifier
        :param project: the project the dataset belong to
        :param name: the name of the dataset
        :param description: a quick  description of the dataset
        """
        self._id = id
        self._project: Project = project
        self._name = name
        self._description = description
        self._connection = connection
        self._resources: Optional[List[str]] = resources
        self._pattern = pattern
        self._client: Client = project._client

    def __repr__(self):
        return f"Dataset(name={self.name}, id={self.id}, description={self.description}, connection={self.connection}, resources={self.resources})"

    @property
    def id(self) -> int:
        """
        Dataset identifier
        :return:
        """
        return self._id

    @id.setter
    def id(self, dataset_id: int):
        self._id = dataset_id

    @property
    def project(self) -> Optional[Project]:
        """
        The project this dataset belong to
        """
        return self._project

    @property
    def name(self) -> str:
        """
        Name of the dataset
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        Quick description of the dataset
        """
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def connection(self) -> Optional[Connection]:
        """
        the connection used to retrieve this dataset
        """
        return self._connection

    @property
    def resources(self) -> Optional[List[str]]:
        """
        the connection used to retrieve this dataset
        """
        return self._resources

    @resources.setter
    def resources(self, resources: List[str]):
        self._resources = resources

    def get_dataset_version(
        self,
        version: Reference,
    ) -> DatasetVersion:
        """
        Gets a specific version of this dataset.

        :param version: The version name or id

        :return: A DatasetVersion or None if the version does not exist
        """
        dataset_version_output = self._client.get_dataset_version(version, self._id)
        try:
            properties: Dict = {
                prop.key: prop.value for prop in self._client.list_dataset_version_properties(version, self._id).list
            }
        except Exception as e:
            logging.warning(f"Properties were not found due to {e}")
            properties = {}
        if dataset_version_output is not None:
            return DatasetVersion(
                dataset=self,
                id=dataset_version_output.id,
                name=dataset_version_output.name,
                description=dataset_version_output.description,
                properties=properties,
                is_starred=dataset_version_output.is_starred,
            )
        else:
            raise RuntimeError(f"The Dataset Version {version} was not found.")

    def create_dataset_version(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_starred: Optional[bool] = None,
        properties: Optional[Dict[str, Any]] = None,
        resources: Optional[List[str]] = None,
        metadata: Optional[Union[List[str], str]] = None,
        attachments: Optional[Union[str, List[str]]] = None,
    ) -> DatasetVersion:
        """
        Create a dataset version.

        Creates a new dataset version

        :param name: The name of the dataset version e.g Changes 'Version 1' to 'name'
        :param description: The description of the dataset version
        :param is_starred: Whether the dataset version is starred
        :param properties: The properties of the dataset version
        :param resources: if connection is set, resources present in connection that should be added to dataset
        :param metadata: if no connection is set, you can add raw metadata to allow versioning of dataset
        :param attachments: list of files to be added to the dataset version (not part of the dataset)

        :return: A DatasetVersion
        """

        dataset_version_input = DatasetVersionInput(name=name, description=description, isStarred=is_starred)
        data_resources = DataResource.create_resources(resources)
        if resources is not None:
            dataset_version_input["resources"] = data_resources
        data_metadata = None
        if metadata is not None:
            try:
                data_metadata = DatasetMetadata.create_gcs(metadata)
            except Exception:
                data_metadata = DatasetMetadata.create_bigquery(metadata)  # type: ignore
            if data_metadata is None:
                raise ValueError("Please provide a valid metadata uri.")
            dataset_version_input["filesMetadata"] = data_metadata
        if properties is not None:
            property_list = [dict(key=k, value=v) for k, v in properties.items()]
            dataset_version_input["properties"] = property_list

        dataset_version_output = self._client.create_dataset_version(dataset_version_input, self._id)
        result = DatasetVersion(
            dataset=self,
            id=dataset_version_output.id,
            name=dataset_version_output.name,
            properties=properties,
            description=dataset_version_output.description,
            is_starred=dataset_version_output.is_starred,
            resources=resources,
            metadata=data_metadata,
        )
        if attachments is not None:
            result.add_attachments(attachments)
        return result

    def update_dataset_version(
        self,
        version: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        is_starred: Optional[bool] = None,
        properties: Optional[Dict] = None,
        resources: Optional[List[str]] = None,
        metadata: Optional[Union[List[str], str]] = None,
    ) -> DatasetVersion:
        """
        Update a dataset version.

        :since:3.0.0

        :param version: The dataset version name or id
        :param name: The name of the dataset version e.g Changes 'Version 1' to 'name'
        :param description: The description of the dataset version
        :param is_starred: Whether the dataset version is starred
        :param properties: The properties of the dataset version
        :param resources: if connection is set, resources present in connection that should be added to dataset
        :param metadata: if no connection is set, you can add raw metadata to allow versioning of dataset
        :return: None
        """
        for prop in self._client.list_dataset_version_properties(version, self._id).list:
            if properties and properties.get(prop.name):
                self._client.update_dataset_version_properties(
                    version, property_id=prop.id, properties={"key": prop.name, "value": prop.value}, dataset=self._id
                )
        dataset_version_output = self._client.get_dataset_version(version, self._id)
        if dataset_version_output is None:
            raise InvalidReferenceError("version", version)
        data_resources = DataResource.create_resources(resources)
        if resources is not None:
            dataset_version_output["resources"] = data_resources
        data_metadata = None
        if metadata is not None:
            try:
                data_metadata = DatasetMetadata.create_gcs(metadata)
            except Exception:
                data_metadata = DatasetMetadata.create_bigquery(metadata)  # type: ignore
            if data_metadata is None:
                raise ValueError("Please provide a valid metadata uri.")
            dataset_version_output["filesMetadata"] = data_metadata
        if name is not None:
            dataset_version_output["name"] = name
        if description is not None:
            dataset_version_output["description"] = description
        if is_starred is not None:
            dataset_version_output["is_starred"] = is_starred
        dataset_version_output = self._client.update_dataset_version(dataset_version_output, version, self._id)
        return DatasetVersion(
            dataset=self,
            id=dataset_version_output.id,
            name=dataset_version_output.name,
            properties=properties,
            description=dataset_version_output.description,
            is_starred=dataset_version_output.is_starred,
            resources=dataset_version_output.get("resources"),
            metadata=data_metadata,
        )

    def list_dataset_versions(
        self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> List[DatasetVersion]:
        """
        List the dataset versions.

        Returns a List of the Dataset Versions associated with the Dataset.
        The DatasetVersion can be used in runs or experiments.

        :param search: The name to search
        :param page_index: The page index
        :param page_size: The page size

        :return: List of DatasetVersions
        """
        dataset_version_output_list = self._client.list_dataset_versions(self._id, search, page_index, page_size)
        return [
            DatasetVersion(
                dataset=self,
                id=dataset_version_output.id,
                name=dataset_version_output.name,
                description=dataset_version_output.description,
                is_starred=dataset_version_output.is_starred,
            )
            for dataset_version_output in dataset_version_output_list.list
        ]

    def delete_dataset_version(
        self,
        version: Reference,
    ) -> None:
        """
        Delete a specific version of this dataset.

        :new_feature:
        :param version: The dataset version name or id
        :return: None
        """
        self._client.delete_dataset_version(version, self._id)
