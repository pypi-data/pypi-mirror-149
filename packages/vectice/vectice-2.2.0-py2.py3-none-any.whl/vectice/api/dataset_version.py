from __future__ import annotations

import urllib
from typing import Optional, TYPE_CHECKING, Dict, Any, List
from urllib.parse import urlencode

from .Page import Page
from ._auth import Auth
from ._http import HttpError
from ._utils import read_nodejs_date
from .dataset import DatasetApi
from .http_error_handlers import HttpErrorHandler
from .json import DatasetVersionOutput, DatasetVersionInput, PagedResponse, TreeItem
from .json.property import PropertyOutput
from .reference import InvalidReferenceError, MissingReferenceError

if TYPE_CHECKING:
    from vectice import Reference


class DatasetVersionApi:
    def __init__(self, auth: Auth):
        self._auth = auth
        self._httpErrorhandler = HttpErrorHandler()

    def get_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetVersionOutput:
        if not isinstance(version, int) and not isinstance(version, str):
            raise ValueError("The dataset version reference is invalid. Please check the entered value.")
        if isinstance(version, int):
            url = f"/metadata/datasetversion/{version}"
        else:
            if dataset is None:
                raise MissingReferenceError("dataset version", "dataset")
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/name/{urllib.parse.quote(version)}"
        try:
            response = self._auth._get(url)
            return DatasetVersionOutput(**response)
        except HttpError as e:
            raise self._httpErrorhandler.handleGetHttpError(e, "dataset version", version)
        except IndexError:
            raise ValueError("The dataset version is invalid. Please check the entered value.")

    def create_dataset_version(
        self,
        data: DatasetVersionInput,
        dataset: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetVersionOutput:
        if isinstance(dataset, int):
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset)
        elif isinstance(dataset, str):
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset, project, workspace)
        else:
            raise InvalidReferenceError("dataset", dataset)
        try:
            data["datasetId"] = parent_dataset.id
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version"
            response = self._auth._post(url, data)
            return DatasetVersionOutput(**response)
        except HttpError as e:
            raise self._httpErrorhandler.handlePostHttpError(e, "dataset version")
        except IndexError:
            raise ValueError("The dataset version is invalid. Please check the entered value.")

    def update_dataset_version(
        self,
        data: DatasetVersionOutput,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetVersionOutput:
        dataset_version_object = self.get_dataset_version(version, dataset, project, workspace)
        url = f"/metadata/datasetversion/{dataset_version_object.id}"
        try:
            response = self._auth._put(url, data)
            return DatasetVersionOutput(**response)
        except HttpError as e:
            raise self._httpErrorhandler.handlePutHttpError(e, "dataset version", version)
        except IndexError:
            raise ValueError("The dataset version is invalid. Please check the entered value.")

    def list_dataset_versions(
        self,
        dataset: Reference,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[DatasetVersionOutput]:
        parent_dataset = DatasetApi(self._auth).get_dataset(dataset, project, workspace)
        url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version"
        queries = {"index": page_index, "size": page_size}
        if search:
            queries["search"] = search
        dataset_versions = self._auth._get(url + "?" + urlencode(queries))
        return PagedResponse(
            item_cls=DatasetVersionOutput,
            total=dataset_versions["total"],
            page=dataset_versions["page"],
            items=dataset_versions["items"],
        )

    def delete_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        try:
            dataset_version = self.get_dataset_version(version, dataset, project, workspace)
            self._auth._delete(f"/metadata/datasetversion/{dataset_version.id}")
        except HttpError as e:
            raise self._httpErrorhandler.handleGetHttpError(e, "dataset version", version)

    def get_files_metadata(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> List[TreeItem]:
        try:
            dataset_version = self.get_dataset_version(version, dataset, project, workspace)
            response = self._auth._get(
                f"/metadata/project/{dataset_version.dataset['project']['id']}/dataset/{dataset_version.dataset_id}/version/{dataset_version.id}/versionFolder"
            )
            return [
                TreeItem(
                    name=item["name"],
                    id=item["id"],
                    path=item["path"]["path"],
                    type=item["type"],
                    isFolder=item["path"]["isFolder"],
                    children=[] if "children" not in item else item["children"],
                    size=int(item["size"]),
                    uri=item["uri"],
                    itemCreatedDate=read_nodejs_date(item["itemCreatedDate"]),
                    itemUpdatedDate=item["itemUpdatedDate"],
                )
                for item in response["files"]
            ]
        except HttpError as e:
            raise self._httpErrorhandler.handleGetHttpError(e, "dataset version", version)

    def create_dataset_version_properties(
        self,
        version: Reference,
        properties: Dict[str, Any],
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        if isinstance(version, int):
            dataset_version = DatasetVersionApi(self._auth).get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/{version}"
        else:
            dataset_version = self.get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/{dataset_version.id}"
        if isinstance(properties, dict):
            self._auth._post(f"{url}/entityProperty/", properties)
        parent_dataset_version = self.get_dataset_version(version, dataset, project, workspace)
        return parent_dataset_version

    def update_dataset_version_properties(
        self,
        version: Reference,
        property_id: int,
        properties: Dict[str, Any],
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        if isinstance(version, int):
            dataset_version = DatasetVersionApi(self._auth).get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version"
        else:
            dataset_version = self.get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/{dataset_version.id}"
        self._auth._put(url + f"/entityProperty/{property_id}", properties)

    def list_dataset_version_properties(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[PropertyOutput]:
        if isinstance(version, int):
            dataset_version = DatasetVersionApi(self._auth).get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/{version}"
        else:
            dataset_version = self.get_dataset_version(version, dataset, project, workspace)
            parent_dataset = DatasetApi(self._auth).get_dataset(dataset_version.dataset_id, project, workspace)
            url = f"/metadata/project/{parent_dataset.project.id}/dataset/{parent_dataset.id}/version/{dataset_version.id}"
        queries = {"index": page_index, "size": page_size}
        model_version_properties = self._auth._get(url + "/entityProperty?" + urlencode(queries))
        properties = [PropertyOutput.from_dict(property).as_dict() for property in model_version_properties["items"]]
        return PagedResponse(
            item_cls=PropertyOutput,
            total=model_version_properties["total"],
            page=model_version_properties["page"],
            items=properties,
        )
