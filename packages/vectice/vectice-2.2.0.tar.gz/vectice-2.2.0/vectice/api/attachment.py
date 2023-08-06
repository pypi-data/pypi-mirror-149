from __future__ import annotations

import urllib
from typing import Optional, List, Tuple, Any, BinaryIO, TYPE_CHECKING

from vectice.api._auth import Auth
from ._http import HttpError
from .http_error_handlers import HttpErrorHandler
from .json import PagedResponse, AttachmentOutput
from vectice.api.code_version import CodeVersionApi
from vectice.api.dataset_version import DatasetVersionApi
from vectice.api.model_version import ModelVersionApi
from vectice.api.run import RunApi
from vectice.api.project import ProjectApi
from .reference import InvalidReferenceError, MissingReferenceError

if TYPE_CHECKING:
    from vectice import Reference


class AttachmentApi:
    def __init__(self, auth: Auth):
        self._auth = auth
        self._httpErrorhandler = HttpErrorHandler()

    def get_attachment(
        self,
        _type: str,
        file_id: int,
        artifact_version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ) -> Optional[BinaryIO]:
        url = None
        if project is None:
            raise MissingReferenceError("attachment", "project")
        parent_project = ProjectApi(self._auth).get_project(project, workspace)
        try:
            if isinstance(artifact_version, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_version}"
            elif isinstance(artifact_version, str):
                if _type == "datasetversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        dataset_version_object = DatasetVersionApi(self._auth).get_dataset_version(
                            version=artifact_version, dataset=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{dataset_version_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "modelversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        model_version_object = ModelVersionApi(self._auth).get_model_version(
                            version=artifact_version, model=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{model_version_object.id}"  # type: ignore
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "codeversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        code_version_object = CodeVersionApi(self._auth).get_code_version(
                            version=artifact_version, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{code_version_object.id}"
                elif _type == "run":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        run_object = RunApi(self._auth).get_run(
                            run=artifact_version, job=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{run_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                # should be relevant for artifacts // parent level
            elif isinstance(artifact, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact}"
            elif isinstance(artifact, str):
                artifact_object = self._auth._get(
                    f"/metadata/project/{parent_project.id}/{_type}/name/{urllib.parse.quote(artifact)}"
                )
                url = f"/metadata/project/{parent_project.id}/{_type}/{artifact_object['id']}/entityfiles"
            else:
                raise MissingReferenceError("attachment", "artifact")
            if url is None:
                raise RuntimeError("url cannot be none")
            return self._auth._get_attachment(url + f"/{file_id}")
        except HttpError as e:
            if artifact_version:
                reference = artifact_version
            elif artifact:
                reference = artifact
            else:
                raise ValueError("No reference to artifact or artifact version provided.")
            raise self._httpErrorhandler.handleGetHttpError(e, _type, reference)

    def post_attachment(
        self,
        _type: str,
        artifact_version: Optional[Reference] = None,
        files: Optional[List[Tuple[str, Tuple[Any, BinaryIO]]]] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
        file_id: Optional[int] = None,
    ) -> None:
        url = None
        if project is None:
            raise MissingReferenceError("attachment", "project")
        parent_project = ProjectApi(self._auth).get_project(project, workspace)
        try:
            if isinstance(artifact_version, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_version}"
            elif isinstance(artifact_version, str):
                if _type == "datasetversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        dataset_version_object = DatasetVersionApi(self._auth).get_dataset_version(
                            version=artifact_version, dataset=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{dataset_version_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "modelversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        model_version_object = ModelVersionApi(self._auth).get_model_version(
                            version=artifact_version, model=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{model_version_object.id}"  # type: ignore
                elif _type == "codeversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        code_version_object = CodeVersionApi(self._auth).get_code_version(
                            version=artifact_version, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{code_version_object.id}"
                elif _type == "run":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        run_object = RunApi(self._auth).get_run(
                            run=artifact_version, job=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{run_object.id}"
                    else:
                        raise MissingReferenceError("attachment", "artifact")
                # should be relevant for artifacts // parent level
            elif isinstance(artifact, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact}"
            elif isinstance(artifact, str):
                artifact_object = self._auth._get(
                    f"/metadata/project/{parent_project.id}/{_type}/name/{urllib.parse.quote(artifact)}"
                )
                url = f"/metadata/project/{parent_project.id}/{_type}/{artifact_object['id']}/entityfiles"
            else:
                raise MissingReferenceError("attachment", "artifact")
            if url is None:
                raise RuntimeError("url cannot be none")
            if file_id:
                url = url + f"/{file_id}"
            if files and len(files) == 1:
                self._auth._post_attachments(url, files)
            elif files and len(files) > 1:
                for file in files:
                    self._auth._post_attachments(url, [file])
        except HttpError as e:
            if artifact_version:
                reference = artifact_version
            elif artifact:
                reference = artifact
            else:
                raise ValueError("No reference to artifact or artifact version provided.")
            self._httpErrorhandler.handleGetHttpError(e, _type, reference)

    def delete_attachment(
        self,
        _type: str,
        artifact_version: Reference,
        file_id: int,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ):
        url = None
        if project is None:
            raise MissingReferenceError("attachment", "project")
        parent_project = ProjectApi(self._auth).get_project(project, workspace)
        try:
            if isinstance(artifact_version, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_version}"
            elif isinstance(artifact_version, str):
                if _type == "datasetversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        dataset_version_object = DatasetVersionApi(self._auth).get_dataset_version(
                            version=artifact_version, dataset=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{dataset_version_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "modelversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        model_version_object = ModelVersionApi(self._auth).get_model_version(
                            version=artifact_version, model=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{model_version_object.id}"  # type: ignore
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "codeversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        code_version_object = CodeVersionApi(self._auth).get_code_version(
                            version=artifact_version, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{code_version_object.id}"
                elif _type == "run":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        run_object = RunApi(self._auth).get_run(
                            run=artifact_version, job=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{run_object.id}"
                    else:
                        raise MissingReferenceError("attachment", "artifact")
            if url is None:
                raise RuntimeError("url cannot be none")
            return self._auth._delete_attachment(url + f"/{file_id}")
        except HttpError as e:
            self._httpErrorhandler.handleGetHttpError(e, _type, artifact_version)

    def list_attachments(
        self,
        _type: str,
        artifact_version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ) -> PagedResponse[AttachmentOutput]:
        url = None
        if project is None:
            raise MissingReferenceError("attachment", "project")
        parent_project = ProjectApi(self._auth).get_project(project, workspace)
        try:
            if isinstance(artifact_version, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_version}"
            elif isinstance(artifact_version, str):
                if _type == "datasetversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        dataset_version_object = DatasetVersionApi(self._auth).get_dataset_version(
                            version=artifact_version, dataset=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{dataset_version_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "modelversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        model_version_object = ModelVersionApi(self._auth).get_model_version(
                            version=artifact_version, model=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{model_version_object.id}"  # type: ignore
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "codeversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        code_version_object = CodeVersionApi(self._auth).get_code_version(
                            version=artifact_version, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{code_version_object.id}"
                elif _type == "run":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        run_object = RunApi(self._auth).get_run(
                            run=artifact_version, job=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{run_object.id}"
                else:
                    raise MissingReferenceError("attachment", "artifact")
                # should be relevant for artifacts // parent level
            elif isinstance(artifact, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact}"
            elif isinstance(artifact, str):
                artifact_object = self._auth._get(
                    f"/metadata/project/{parent_project.id}/{_type}/name/{urllib.parse.quote(artifact)}"
                )
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_object['id']}"
            else:
                raise MissingReferenceError("attachment", "artifact")
        except HttpError as e:
            if artifact_version:
                reference = artifact_version
            elif artifact:
                reference = artifact
            else:
                raise ValueError("No reference to artifact or artifact version provided.")
            self._httpErrorhandler.handleGetHttpError(e, _type, reference)
        if url is None:
            raise InvalidReferenceError("artifact", artifact)
        attachments = self._auth._list_attachments(url)
        return PagedResponse(
            item_cls=AttachmentOutput,
            total=len(attachments),
            page={},
            items=attachments,
        )

    def update_attachments(
        self,
        _type: str,
        files: List[Tuple[str, Tuple[Any, BinaryIO]]],
        artifact_version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ):
        url = None
        if project is None:
            raise MissingReferenceError("attachment", "project")
        parent_project = ProjectApi(self._auth).get_project(project, workspace)
        try:
            attachments = {
                attach.fileName: attach.fileId
                for attach in self.list_attachments(_type, artifact_version, artifact, workspace, project).list
            }
            if isinstance(artifact_version, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_version}"
            elif isinstance(artifact_version, str):
                if _type == "datasetversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        dataset_version_object = DatasetVersionApi(self._auth).get_dataset_version(
                            version=artifact_version, dataset=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{dataset_version_object.id}"
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "modelversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        model_version_object = ModelVersionApi(self._auth).get_model_version(
                            version=artifact_version, model=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{model_version_object.id}"  # type: ignore
                    else:
                        raise MissingReferenceError("artifact version", "artifact")
                elif _type == "codeversion":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        code_version_object = CodeVersionApi(self._auth).get_code_version(
                            version=artifact_version, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{code_version_object.id}"
                elif _type == "run":
                    if isinstance(artifact, int) or isinstance(artifact, str):
                        run_object = RunApi(self._auth).get_run(
                            run=artifact_version, job=artifact, project=project, workspace=workspace
                        )
                        url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{run_object.id}"
                    else:
                        raise MissingReferenceError("attachment", "artifact")
                # should be relevant for artifacts // parent level
            elif isinstance(artifact, int):
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact}"
            elif isinstance(artifact, str):
                artifact_object = self._auth._get(
                    f"/metadata/project/{parent_project.id}/{_type}/name/{urllib.parse.quote(artifact)}"
                )
                url = f"/metadata/project/{parent_project.id}/entityfiles/{_type}/{artifact_object['id']}"
            else:
                raise MissingReferenceError("attachment", "artifact")
            if url is None:
                raise InvalidReferenceError("artifact", artifact)
            for file in files:
                file_name = file[1][0]
                file_id = attachments.get(file_name)
                if file_id:
                    self._auth._put_attachments(url + f"/{file_id}", [file])
        except HttpError as e:
            if artifact_version:
                reference = artifact_version
            elif artifact:
                reference = artifact
            else:
                raise ValueError("No reference to artifact or artifact version provided.")
            self._httpErrorhandler.handleGetHttpError(e, _type, reference)
