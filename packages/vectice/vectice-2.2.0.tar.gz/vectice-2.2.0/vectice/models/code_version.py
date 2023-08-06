from __future__ import annotations

import logging
import os
from typing import Optional, List, Union, BinaryIO, TYPE_CHECKING, Tuple

from vectice.api.client import Client
from .attachment_container import AttachmentContainer
from .git_version import GitVersion

if TYPE_CHECKING:
    from vectice import Reference
    from vectice.models.project import Project


# @dataclass
# class __CodeData:
#     gitVersion: GitVersion
#     """
#     git information structure extracted automatically by the SDK.
#     """


class CodeVersion(AttachmentContainer):
    """
    Code version class
    """

    def __init__(
        self,
        project: Project,
        id: Optional[int] = None,  # for rule API
        code_id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        uri: Optional[str] = None,
        is_starred: Optional[bool] = False,
        attachments: Optional[Union[str, List[str]]] = None,
        git_version_id: Optional[int] = None,
        git_version: Optional[GitVersion] = None,
        version: Optional[Reference] = None,
    ):
        self._project = project
        self._id = id
        self._description = description
        self._uri = uri
        self._isStarred = is_starred
        self._name = name  # Version name
        self._attachments: Optional[
            Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]
        ] = None
        self._client: Client = self._project._client
        self._version = version
        self._git_version_id = git_version_id
        self._git_version = git_version
        self._code_id = code_id

        if git_version is None:
            pass
        if attachments:
            self.add_attachments(attachments)

    def __repr__(self):
        return f"CodeVersion(id={self.id}, name={self.name}, description={self.description}, uri={self.uri}, gitVersion={self.git_version}, project={self.project})"

    @property
    def project(self) -> Project:
        return self._project

    @property
    def id(self) -> int:
        """
        The code identifier
        :return:
        """
        if self._id is None:
            raise RuntimeError("can not use id as the code version is not saved")
        return self._id

    @property
    def code_id(self) -> Optional[int]:
        """
        The code identifier
        :return:
        """
        return self._code_id

    @property
    def name(self) -> Optional[str]:
        """
        Name of the code
        """
        return self._name

    @property
    def version(self) -> Optional[Reference]:
        return self._version

    @property
    def description(self) -> Optional[str]:
        """
        Quick description of the code
        """
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def uri(self) -> Optional[str]:
        return self._uri

    @uri.setter
    def uri(self, uri: str):
        self._uri = uri

    @property
    def is_starred(self) -> Optional[bool]:
        return self._isStarred

    @is_starred.setter
    def is_starred(self, is_starred: bool):
        self._isStarred = is_starred

    @property
    def attachments(self) -> Optional[Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]]:
        return self._attachments

    @attachments.setter
    def attachments(self, attachments: Union[Tuple[str, Tuple[str, BinaryIO]], List[Tuple[str, Tuple[str, BinaryIO]]]]):
        self._attachments = attachments

    @property
    def git_version_id(self) -> Optional[int]:
        return self._git_version_id

    @property
    def git_version(self) -> Optional[GitVersion]:
        return self._git_version

    def add_attachments(self, file_path: Union[str, List[str]]):
        """
        add an attachment to the entity

        :param file_path:
        """
        attachments = []
        if isinstance(file_path, list):

            for file in file_path:
                try:
                    if not os.path.exists(file):
                        raise ValueError(f"the file path {file} is not valid. the file does not exist")
                    curr_file = ("file", (file, open(file, "rb")))
                    attachments.append(curr_file)
                except Exception:
                    logging.warning(f"Did not read {file}.")
        else:
            if not os.path.exists(file_path):
                raise ValueError(f"the file path {file_path} is not valid. the file does not exist")
            attachments = [("file", (file_path, open(file_path, "rb")))]
        self._client.create_attachments("codeversion", attachments, self.id)

    def delete_attachments(self, file_path: Union[List[str], str]):
        """
        remove an attachment from the entity

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
        try:
            attachment_list = {
                attach.fileName: attach.fileId for attach in self._client.list_attachments("codeversion", self.id).list
            }
        except Exception as e:
            raise ValueError(f"Codeversion attachment failed to retrieve. Due to {e}")
        for file in attachments:
            file_name = file[1][0]
            file_id = attachment_list.get(file_name)
            if file_id:
                self._client.delete_attachment("codeversion", self.id, file_id)

    def get_attachment(self, file_path: Union[List[str], str]) -> Optional[BinaryIO]:
        """
        get an attachment from the entity

        :param file_path:
        """
        attachments: List[str] = []
        if isinstance(file_path, str):
            attachments.append(file_path)
        else:
            attachments = file_path

        try:
            attachment_list = {
                attach.fileName: attach.fileId for attach in self._client.list_attachments("codeversion", self.id).list
            }
        except Exception as e:
            raise ValueError(f"CodeVersion attachment failed to retrieve. Due to {e}")
        for file in attachments:
            file_id = attachment_list.get(file)
            if file_id:
                return self._client.get_attachment(
                    "codeversion",
                    file_id,
                    None,
                    self.id,
                )
            else:
                raise ValueError(f"Failed to get attachment named '{file}'. Please check the filename.")
        return None

    def list_attachments(self):
        """
        List attachments of the entity

        """
        return self._client.list_attachments(
            "codeversion", self.id, None, self._client.workspace.id, self._client.project.id
        )

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
        self._client.update_attachments("codeversion", attachments, self.id)
