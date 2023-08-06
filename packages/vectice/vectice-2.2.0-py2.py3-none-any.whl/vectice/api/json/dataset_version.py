from datetime import datetime
from typing import Optional, cast

from vectice.api._utils import read_nodejs_date


class DatasetVersionInput(dict):
    @property
    def dataset_id(self) -> int:
        return int(self["datasetId"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str:
        return str(self["description"])

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def resources(self) -> str:
        return str(self["resources"])

    @property
    def files_metadata(self) -> str:
        return str(self["filesMetadata"])

    @property
    def is_starred(self) -> str:
        return str(self["isStarred"])

    @property
    def properties(self) -> str:
        return str(self["properties"])


class DatasetVersionOutput(dict):
    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def created_date(self) -> Optional[datetime]:
        return read_nodejs_date(str(self["createdDate"]))

    @property
    def updated_date(self) -> Optional[datetime]:
        return read_nodejs_date(str(self["updatedDate"]))

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def version(self) -> int:
        return int(self["version"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> Optional[str]:
        if "description" in self and self["description"] is not None:
            return str(self["description"])
        else:
            return None

    @property
    def uri(self) -> str:
        return str(self["uri"])

    @property
    def author_id(self) -> int:
        return int(self["authorId"])

    @property
    def deleted_date(self) -> Optional[datetime]:
        return read_nodejs_date(str(self["deletedDate"]))

    @property
    def version_type(self) -> int:
        return int(self["versionType"])

    @property
    def version_number(self) -> int:
        return int(self["versionNumber"])

    @property
    def dataset_id(self) -> int:
        return int(self["dataSetId"])

    @property
    def version_folder_id(self) -> int:
        return int(self["versionFolderId"])

    @property
    def origin_id(self) -> int:
        return int(self["originId"])

    @property
    def is_starred(self) -> bool:
        return bool(self["isStarred"])

    @property
    def dataset(self) -> dict:
        return cast(dict, self["dataSet"])

    @property
    def files_metadata(self) -> dict:
        return cast(dict, self["filesMetadata"])
