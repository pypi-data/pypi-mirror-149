from __future__ import annotations

from typing import Optional, TYPE_CHECKING, List, Dict

from vectice.api import Client
from vectice.api.json import RunInput, JobType
from .integration import AbstractIntegration

from .run import Run
from ..api.json.property import create_properties_input

if TYPE_CHECKING:
    from vectice.models import Project
    from vectice import Reference

import inspect


class Job:
    def __init__(
        self, name: str, id: int, project: Project, description: Optional[str] = None, type: JobType = JobType.OTHER
    ):
        """
        :param id:Job identifier
        :param project: The project this job belong to
        :param name: Name of the job
        :param description: Quick description of the job
        :param type: type of Job it can be "EXTRACTION"|"PREPARATION"|"TRAINING"|"INFERENCE"|"DEPLOYMENT"|"OTHER"
        """
        self._id = id
        self._project: Project = project
        self._name: str = name
        self._description: Optional[str] = description
        self._type: JobType = type
        self._client: Client = project._client
        self._integration_client: Optional[AbstractIntegration] = project._integration_client

    def __repr__(self):
        return f"Job(name={self.name}, id={self.id}, description={self.description}, type={self.type})"

    @property
    def id(self):
        """
        Job identifier
        """
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def project(self) -> Project:
        """
        The project this job belongs to
        """
        return self._project

    @project.setter
    def project(self, project):
        self._project = project

    @property
    def name(self):
        """
        Name of the job
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def type(self):
        """
        The job type
        """
        return self._type

    @type.setter
    def type(self, job_type):
        self._type = job_type

    @property
    def description(self):
        """
        Quick description of the job
        """
        return self._description

    @description.setter
    def description(self, description):
        self._description = description

    @classmethod
    def from_dict(cls, env):
        return cls(**{k: v for k, v in env.items() if k in inspect.signature(cls).parameters})

    def create_run(
        self,
        name: Optional[str] = None,
        properties: Optional[Dict] = None,
        auto_code: bool = False,
        check_remote_repository: bool = True,
        notes: Optional[str] = None,
        system_name: Optional[str] = None,
    ) -> Run:
        """
        Create a run.
        Creates a run in the specified project with the information passed to this method.
        The run is not viewable in the Vectice platform until the job is started.
        See :class:`Run` for more information
        :param name: The run name.
        :param properties: Properties of the run
        :param auto_code: indicate if auto code should be used or not
        :param check_remote_repository: indicate if we should check remote repository on code version creation
        :return: Run
        """
        data = RunInput(name=name, properties=properties, description=notes, systemName=system_name)
        run_output = self._client.create_run(data, self._id)
        if properties:
            self._client.create_run_properties(run_output.id, create_properties_input(properties))
        return Run(
            run_output.id,
            self,
            run_output.name,
            run_output.system_name,
            run_output.start_date,
            run_output.end_date,
            run_output.status,
            auto_code=auto_code,
            check_remote_repository=check_remote_repository,
            description=run_output.description,
            properties=properties,
        )

    def delete_run(self, run: Reference) -> None:
        """
        Delete the specified run.
        The run must be part of this job.
        :new_feature:
        :param run: The run name or id
        :return: None
        """
        self._client.delete_run(run, self.id)

    def get_run(
        self,
        run: Reference,
    ) -> Run:
        """
        get a Run.
        :since:3.0.0
        :param run: The run name or id
        :return: A Run
        """
        run_output = self._client.get_run(run, self._id)
        return Run(
            run_output.id,
            self,
            run_output.name,
            run_output.system_name,
            run_output.start_date,
            run_output.end_date,
            run_output.status,
        )

    def update_run(
        self,
        run: Reference,
        name: Optional[str] = None,
        system_name: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Run:
        """
        Update a run with the new attributes values.
        :param run: The run name or id
        :param name: The name of the job
        :param system_name: The name of the system
        :param status: The status of the run
        :return: None
        """
        run_output = self._client.get_run(run, self._id)
        if name is not None and name != run_output.name:
            run_output["name"] = name
        if system_name is not None and system_name != run_output.system_name:
            run_output["systemName"] = system_name
        if status is not None and status != run_output.status:
            run_output["status"] = status
        updated_output = self._client.update_run(run_output)
        return Run(
            updated_output.id,
            self,
            updated_output.name,
            updated_output.system_name,
            updated_output.start_date,
            updated_output.end_date,
            updated_output.status,
        )

    def list_runs(
        self,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> List[Run]:
        """
        Lists the runs in this job.

        :param search: The name to search
        :param page_index: The page index
        :param page_size: The page size

        :return: the list of Run of this jobs
        """
        outputs = self._client.list_runs(self.id, None, None, search, page_index, page_size)
        return [
            Run(
                run_output.id,
                self,
                run_output.name,
                run_output.system_name,
                run_output.start_date,
                run_output.end_date,
                run_output.status,
            )
            for run_output in outputs.list
        ]
