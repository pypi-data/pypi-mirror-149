from __future__ import annotations

import logging
import os
from typing import Optional, Union, List, Dict, BinaryIO, TYPE_CHECKING, Tuple, Any

from vectice.api.client import Client
from ..api.json import ArtifactVersion, TreeItem

if TYPE_CHECKING:
    from vectice.models import Dataset


class DatasetVersion:
    """
    dataset - dataset id or name. Previously parentName or parentId -> backend needs parentName or parentId *NB
    """

    def __init__(
        self,
        dataset: Dataset,
        id: int,
        name: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        resources: Optional[Union[str, List[str]]] = None,
        metadata: Optional[List[TreeItem]] = None,
        attachments: Optional[Union[str, List[str]]] = None,
        auto_version: Optional[bool] = True,
        is_starred: Optional[bool] = False,
        version: Optional[ArtifactVersion] = None,
    ):
        self._dataset = dataset
        self._id = id
        self._description = description
        self._isStarred = is_starred
        self._autoVersion = auto_version
        self._name = name  # Version name
        self._properties = properties
        self._version = version  # Relevant for runs // ArtifactVersion
        self._resources = resources
        self._filesMetadata = metadata
        self._parentId = dataset.id
        self._attachments: Optional[
            Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]
        ] = None
        self._client: Client = dataset._client

        if properties:
            self.properties = properties
        if version:
            if isinstance(version, str):
                self.version = ArtifactVersion(versionNumber=None, versionName=version, id=None)
            elif isinstance(version, int):
                self.version = ArtifactVersion(versionNumber=version, versionName=None, id=None)
        if attachments:
            self.add_attachments(attachments)

    def __repr__(self):
        return f"DatasetVersion(dataset={self.dataset}, id={self.id}, description={self.description}, is_starred={self.is_starred}, auto_version={self.auto_version}, name={self.name}, properties={self.properties}, version={self.version}, resources={self.resources}, metadata={self.files_metadata}, attachments={self.attachments})"

    @property
    def dataset(self) -> Dataset:
        return self._dataset

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, dataset_version_id: int):
        self._id = dataset_version_id

    @property
    def name(self) -> Optional[str]:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def parent_name(self) -> Optional[str]:
        return self._dataset.name

    @property
    def parent_id(self) -> Optional[int]:
        return self._dataset.id

    @parent_id.setter
    def parent_id(self, dataset: int):
        self._parentId = dataset

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
    def properties(self) -> Optional[Dict]:
        return self._properties

    @properties.setter
    def properties(self, properties: Dict[str, Any]):
        self._properties = properties

    @property
    def resources(self) -> Optional[Union[str, List[str]]]:
        return self._resources

    @resources.setter
    def resources(self, resources: Union[str, List[str]]):
        self._resources = resources

    @property
    def files_metadata(self) -> Optional[List[TreeItem]]:
        return self._filesMetadata

    @files_metadata.setter
    def files_metadata(self, files_metadata: List[TreeItem]):
        self._filesMetadata = files_metadata
        self._attachments = None

    @property
    def is_starred(self) -> Optional[bool]:
        return self._isStarred

    @is_starred.setter
    def is_starred(self, is_starred: bool):
        self._isStarred = is_starred

    @property
    def auto_version(self) -> Optional[bool]:
        return self._autoVersion

    @auto_version.setter
    def auto_version(self, auto_version: bool):
        self._autoVersion = auto_version

    @property
    def version(self) -> Optional[ArtifactVersion]:
        return self._version

    @version.setter
    def version(self, version: ArtifactVersion):
        self._version = version

    @property
    def attachments(self) -> Optional[Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]]:
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]):
        self._attachments = attachments

    def add_attachments(self, file_path: Union[str, List[str]]):
        """
        add an attachment to the entity

        :param file_path:
        """
        attachments = []
        attached_files = self.list_attachments()
        if isinstance(file_path, list):
            for file in file_path:
                try:
                    if not os.path.exists(file):
                        raise ValueError(f"the file path {file} is not valid. the file does not exist")
                    curr_file = ("file", (file, open(file, "rb")))
                    attachments.append(curr_file)
                    if file_path in attached_files:
                        raise RuntimeError(f"{file_path} is already attached to '{self.name}'")
                except Exception:
                    logging.warning(f"Did not read {file}.")
        else:
            if not os.path.exists(file_path):
                raise ValueError(f"the file path {file_path} is not valid. the file does not exist")
            attachments = [("file", (file_path, open(file_path, "rb")))]
        if file_path in attached_files:
            raise RuntimeError(f"{file_path} is already attached to '{self.name}'")
        self._client.create_attachments("datasetversion", attachments, self.id)

    def update_attachments(self, file_path: Union[str, List[str]]):
        """
        add an attachment to the entity

        :param file_path:
        """
        attachments = []
        if isinstance(file_path, list):

            for file in file_path:
                try:
                    curr_file = ("file", (file, open(file, "rb")))
                    attachments.append(curr_file)
                except Exception:
                    logging.warning(f"Did not read {file}.")
        else:
            attachments = [("file", (file_path, open(file_path, "rb")))]
        self._client.update_attachments("datasetversion", attachments, self.id)

    def list_attachments(self) -> List[str]:
        """
        List attachments of the entity

        """
        attachments = self._client.list_attachments("datasetversion", self.id)
        files = []
        for attachment in attachments.list:
            files.append(attachment.fileName)
        return files

    def delete_attachments(self, file_path: Union[List[str], str]):
        """
        remove an attachment from the entity

        :param file_path:
        """
        attachments: List[str] = []
        if isinstance(file_path, str):
            attachments.append(file_path)
        else:
            attachments = file_path

        try:
            attachment_list = {
                attach.fileName: attach.fileId
                for attach in self._client.list_attachments("datasetversion", self.id).list
            }
        except Exception as e:
            raise ValueError(f"DatasetVersion attachment failed to retrieve. Due to {e}")
        for file in attachments:
            file_id = attachment_list.get(file)
            if file_id:
                self._client.delete_attachment("datasetversion", self.id, file_id, self.parent_id)

    def get_files_metadata(self) -> List[TreeItem]:
        return self._client.get_dataset_version_files_metadata(self.id)
