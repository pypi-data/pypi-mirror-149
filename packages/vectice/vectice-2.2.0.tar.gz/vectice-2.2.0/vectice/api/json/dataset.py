from typing import Optional

from .artifact_version import ArtifactVersion
from .connection import ConnectionOutput
from .project import ProjectOutput


class DatasetInput(dict):
    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def pattern(self) -> str:
        return str(self["pattern"])

    @property
    def description(self) -> Optional[str]:
        if "description" in self and self["description"] is not None:
            return str(self["description"])
        else:
            return None

    @property
    def connection_id(self) -> int:
        return int(self["connectionId"])

    @property
    def connection_name(self) -> str:
        return str(self["connectionName"])

    @property
    def version(self) -> ArtifactVersion:
        return ArtifactVersion(**self["version"])


class DatasetOutput(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "project" in self:
            self._project: ProjectOutput = ProjectOutput(**self["project"])
        else:
            self._project = None
        if "connection" in self:
            self._connection: ConnectionOutput = ConnectionOutput(**self["connection"])
        else:
            self._connection = None

    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def id(self) -> int:
        return int(self["id"])

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def description(self) -> str:
        return str(self["description"])

    @property
    def pattern(self) -> str:
        return str(self["pattern"])

    @property
    def is_pattern_base(self) -> str:
        return str(self["isPatternBase"])

    @property
    def create_date(self) -> str:
        return str(self["createdDate"])

    @property
    def updated_date(self) -> str:
        return str(self["updatedDate"])

    @property
    def deleted_date(self) -> str:
        return str(self["deletedDate"])

    @property
    def connection_id(self) -> Optional[int]:
        return int(self["connectionId"])

    @property
    def created_by_user_id(self) -> int:
        return int(self["createdByUserId"])

    @property
    def project_id(self) -> int:
        return int(self["projectId"])

    @property
    def version(self) -> int:
        return int(self["version"])

    @property
    def connection(self) -> Optional[ConnectionOutput]:
        return self._connection

    @property
    def project(self) -> ProjectOutput:
        return self._project

    @project.setter
    def project(self, project: ProjectOutput):
        self._project = project
