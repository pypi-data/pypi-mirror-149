from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from vectice.models import Workspace


class Connection:
    """
    Connection to a repository that contains datasets
    :since:3.0.0
    """

    def __init__(
        self,
        id: int,
        name: str,
        workspace: Workspace,
        type: str,
        description: Optional[str] = None,
    ):
        """
        :since:3.0.0
        :param id: connection identifier
        :param name: name of the connection
        :param workspace: the workspace the connection belong to
        :param type: the type of connection
        :param description: the description of the connection
        """
        self._id = id
        self._name = name
        self._workspace = workspace
        self._type = type
        self._description = description

    def __repr__(self):
        return f"Connection(id={self.id}, name={self.name}, type={self.type}, description={self.description}, workspace={self.workspace})"

    @property
    def id(self) -> int:
        """
        connection identifier
        """
        return self._id

    @property
    def name(self) -> str:
        """
        name of the connection
        """
        return self._name

    @property
    def workspace(self) -> Workspace:
        """
        The workspace this connection belong to
        :return:
        """
        return self._workspace

    @property
    def type(self) -> str:
        """
        type of the connection
        """
        return self._type

    @property
    def description(self) -> Optional[str]:
        """
        description of the connection
        """
        return self._description
