from __future__ import annotations

from typing import List, Optional, Dict, TYPE_CHECKING

from vectice.api.json import ProjectInput, ConnectionInput
from .connection import Connection
from .project import Project

if TYPE_CHECKING:
    from vectice import Reference
    from vectice.api import Client
    from vectice.models.integration import AbstractIntegration


class Workspace:
    """
    Workspace is a space where you can found :py:class:`Project` and :py:class:`Connection` for a team.

    In a workspace, you can manage (create, update, delete, get and list ) projects.

    You can also lists and get connections but you can not create or delete them.

    :new_feature:
    """

    def __init__(self, id: int, name: str, description: Optional[str] = None):
        """
        :param id: the workspace identifier
        :param name: the name of the workspace
        :param description: the description of the workspace
        """
        self._id = id
        self._name = name
        self._description = description
        self._client: Client

    def __post_init__(self, client: Client, integration_client: Optional[AbstractIntegration]):
        self._client = client
        self._integration_client = integration_client

    def __repr__(self):
        return f"Workspace(name={self.name}, id={self.id}, description={self.description})"

    @property
    def id(self) -> int:
        """
        the workspace identifier
        :return:
        """
        return self._id

    @property
    def name(self) -> str:
        """
        the name of the workspace
        :return:
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        the description of the workspace
        :return:
        """
        return self._description

    def create_project(self, name: str, description: Optional[str] = None) -> Project:
        """
        Creates a new project in the workspace with the given attributes.
        the name is required and must be unique in the workspace.

        By default, the project is public, change `is_public` to `False`
        to make it private.
        the status can be `New`, `InProgress` or `Deployed`

        :new_feature:

        :param name: The name of the project to be created.
        :param is_public: Whether the project is public or private
        :param status: The status of the project
        :param description: The description of the project

        :return: The newly created project
        """
        data = ProjectInput(name=name, description=description)
        output = self._client.create_project(data, self.id)
        return Project(output.id, self, output.name, output.description)

    def update_project(
        self,
        project: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Project:
        """
        Update a project.

        :new_feature:

        :param project: The project name or id to update.
        :param name: The name of the project to be.
        :param is_public: Whether the project is public or private
        :param description: The description of the project
        :param status: The status of the project

        :return: the updated project
        """
        data = ProjectInput(name=name, description=description)
        project_object = self.get_project(project)
        output = self._client.update_project(data, project_object.id, self.id)
        return Project(output.id, self, output.name, output.description)

    def get_project(self, project: Reference) -> Project:
        """
        Get a project.

        Gets a project instance with the specified project name or id in the current workspace.

        :new_feature:

        :param project: The project name or id to get.

        :return: a project
        """
        item = self._client.get_project(project, self.id)
        return Project(item.id, self, item.name, item.description)

    def delete_project(self, project: Reference) -> None:
        """
        Delete the project specified by the user.

        :new_feature:

        :param project: The project name or id to delete.

        :return: None
        """
        project_object = self.get_project(project)
        self._client.delete_project(project_object.id)

    def list_projects(
        self,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> List[Project]:
        """
        List the projects in this workspace.

        :new_feature: SC-20267

        :param search: The name to search
        :param page_index: The page index
        :param page_size: The page size

        :return: a list of projects
        """
        response = self._client.list_projects(self.id, search, page_index, page_size)
        return [Project(item.id, self, item.name, item.description) for item in response.list]

    def list_connections(
        self,
        connection_type: Optional[str] = None,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> List[Connection]:
        """
        List the connections defined in this workspace.

        :param search: The name to search
        :param page_index: The page index
        :param page_size: The page size

        :return: a list of connections
        """
        response = self._client.list_connections(self.id, connection_type, search, page_index, page_size)
        return [Connection(item.id, item.name, self, item.type, item.description) for item in response.list]

    def get_connection(self, connection: Reference) -> Connection:
        """
        Get a connection.

        Gets a connection instance with the specified connection name or id in the current workspace.

        :new_feature:

        :param connection: The connection name or id to get.

        :return: a connection
        """
        item = self._client.get_connection(connection, self.id)
        return Connection(item.id, item.name, self, item.type, item.description)

    def create_connection(
        self, name: str, type: str, parameters: Dict, description: Optional[str] = None
    ) -> Connection:
        """
        create a connection.

        create a connection with the specified connection name, description and
        parameters. The parameters keys and values depends on each connection Type.

        :new_feature:

        :param name: name of the connection
        :param type: the type of connection
        :param parameters: the parameters for the connection
        :param description: the description of the connection

        :return: a connection
        """
        data = ConnectionInput(name=name, parameters=parameters, type=type, description=description)
        output = self._client.create_connection(data, self.id)
        return Connection(output.id, output.name, self, output.type, output.description)

    def delete_connection(self, connection: Reference) -> None:
        """
        Delete the connection.
        :new_feature:
        :param connection: The connection name or id to delete.
        :return: None
        """
        self._client.delete_connection(connection, self.id)

    def update_connection(
        self,
        connection: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        parameters: Optional[Dict[str, str]] = None,
    ) -> Connection:
        connection_input = ConnectionInput(name=name, description=description, parameters=parameters)
        connection_update = self._client.update_connection(connection_input, connection, self.id)
        return Connection(
            connection_update.id, connection_update.name, self, connection_update.type, connection_update.description
        )
