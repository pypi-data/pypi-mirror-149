from typing import Optional, Dict


class ConnectionInput(dict):
    def items(self):
        result = []
        for key in self:
            if self[key] is not None:
                result.append((key, self[key]))
        return result

    @property
    def name(self) -> str:
        return str(self["name"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def parameters(self) -> Dict[str, str]:
        return dict(self["parameters"])

    @property
    def description(self) -> Optional[str]:
        if "description" in self and self["description"] is not None:
            return str(self["description"])
        else:
            return None


class ConnectionOutput(dict):
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
    def status(self) -> str:
        return str(self["status"])

    @property
    def type(self) -> str:
        return str(self["type"])

    @property
    def workspace_id(self) -> int:
        return int(self["workspaceId"])

    @property
    def description(self) -> Optional[str]:
        if "description" in self and self["description"] is not None:
            return str(self["description"])
        else:
            return None
