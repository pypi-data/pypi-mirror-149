from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING, Tuple, BinaryIO, Any, Dict, Sequence

from vectice.api.Page import Page
from vectice.api._auth import Auth
from vectice.api.artifact import ArtifactApi
from vectice.api.code import CodeApi
from vectice.api.code_version import CodeVersionApi
from vectice.api.connections import ConnectionApi
from vectice.api.dataset import DatasetApi
from vectice.api.dataset_version import DatasetVersionApi
from vectice.api.job import JobApi
from vectice.api.json_object import JsonObject
from vectice.api.run import RunApi
from .attachment import AttachmentApi
from .json import (
    ModelVersionOutput,
    ModelVersionInput,
    PagedResponse,
    ModelOutput,
    ModelInput,
    JobInput,
    ArtifactOutput,
    ProjectInput,
    ConnectionInput,
    StartRunInput,
    StopRunInput,
    StopRunOutput,
    TreeItem,
)
from .json.metric import MetricInput, MetricOutput
from .json.property import PropertyOutput, PropertyInput
from .json.rule import ArtifactReferenceInput, FillRunInput
from .json.workspace import WorkspaceInput
from .model import ModelApi
from .model_version import ModelVersionApi
from .project import ProjectApi
from .reference import MissingReferenceError
from .rule import RuleApi
from .workspace import WorkspaceApi

if TYPE_CHECKING:
    from vectice import Reference
    from .json import JobOutput
    from .json import RunOutput, RunInput
    from .json import WorkspaceOutput
    from .json import ProjectOutput
    from .json import ArtifactInput
    from .json import ConnectionOutput
    from .json import DatasetInput, DatasetOutput
    from .json import DatasetVersionOutput, DatasetVersionInput
    from .json import AttachmentOutput
    from .json import CodeOutput, CodeInput
    from .json import CodeVersionOutput, CodeVersionInput


class Client:
    """
    Low level Vectice API client.
    """

    def __init__(
        self,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
        token: Optional[str] = None,
        api_endpoint: Optional[str] = None,
        auto_connect=True,
        allow_self_certificate=True,
    ):
        self._auth = Auth(
            api_endpoint=api_endpoint,
            api_token=token,
            auto_connect=auto_connect,
            allow_self_certificate=allow_self_certificate,
        )
        self._workspace = None
        self._project = None
        if auto_connect and workspace is not None:
            if isinstance(project, int):
                self._project = self.get_project(project)
                self._workspace = self._project.workspace
                if workspace is not None:
                    if isinstance(workspace, str):
                        if workspace != self._workspace.name:
                            raise ValueError(
                                f"Inconsistency in configuration: project {project} does not belong to workspace {workspace}"
                            )
                    else:
                        if workspace != self._workspace.id:
                            raise ValueError(
                                f"Inconsistency in configuration: project {project} does not belong to workspace {workspace}"
                            )
            else:
                self._workspace = self.get_workspace(workspace)
                if project is not None:
                    self._project = self.get_project(project, workspace)
        elif auto_connect and workspace is None and project:
            self._project = self.get_project(project)
            if self._project is not None:
                self._workspace = self._project.workspace

    @property
    def workspace(self) -> Optional[WorkspaceOutput]:
        return self._workspace

    @property
    def project(self) -> Optional[ProjectOutput]:
        return self._project

    def create_project(self, data: ProjectInput, workspace: Reference) -> ProjectOutput:
        return ProjectApi(self._auth).create_project(data, workspace)

    def delete_project(self, project: Reference, workspace: Optional[Reference] = None):
        return ProjectApi(self._auth).delete_project(project, workspace)

    def update_project(self, data: ProjectInput, project: Reference, workspace: Reference) -> ProjectOutput:
        return ProjectApi(self._auth).update_project(data, project, workspace)

    def list_projects(
        self,
        workspace: Reference,
        search: Optional[str] = None,
        page_index: int = Page.index,
        page_size: int = Page.size,
    ) -> PagedResponse[ProjectOutput]:
        return ProjectApi(self._auth).list_projects(workspace, search, page_index, page_size)

    def get_project(self, project: Reference, workspace: Optional[Reference] = None) -> ProjectOutput:
        return ProjectApi(self._auth).get_project(project, workspace)

    def get_workspace(self, workspace: Reference) -> WorkspaceOutput:
        return WorkspaceApi(self._auth).get_workspace(workspace)

    def create_workspace(self, data: WorkspaceInput) -> WorkspaceOutput:
        return WorkspaceApi(self._auth).create_workspace(data)

    def update_workspace(self, data: WorkspaceInput, workspace: Reference) -> WorkspaceOutput:
        return WorkspaceApi(self._auth).update_workspace(data, workspace)

    def list_workspaces(
        self, search: Optional[str] = None, page_index: int = 1, page_size: int = 20
    ) -> PagedResponse[WorkspaceOutput]:
        return WorkspaceApi(self._auth).list_workspaces(search, page_index, page_size)

    def get_job(
        self, job: Reference, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> JobOutput:
        if isinstance(job, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return JobApi(self._auth).get_job(job, project, workspace)

    def delete_job(
        self, job: Reference, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> None:
        if isinstance(job, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return JobApi(self._auth).delete_job(job, project, workspace)

    def start_run(
        self, data: StartRunInput, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> JsonObject:
        """
        Start a run.

        :param run: The run to start
        :param inputs: A list of artifacts to linked to the run
        :return: A json object
        """
        if project is None and self._project is not None:
            project = self._project.id
        if project is None:
            raise MissingReferenceError("run", "project")
        return RuleApi(self._auth).start_run(data, project, workspace)

    def fill_run(
        self,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        inputs: Optional[List[ArtifactReferenceInput]] = None,
        outputs: Optional[List[ArtifactReferenceInput]] = None,
    ):
        if inputs is not None or outputs is not None:
            run_object = self.get_run(run, job, project, workspace)
            return RuleApi(self._auth).fill_run(
                FillRunInput(run_object.id, [] if inputs is None else inputs, [] if outputs is None else outputs)
            )

    def stop_run(
        self,
        data: StopRunInput,
    ) -> StopRunOutput:
        """

        :param run:
        :param outputs:
        :return:
        """
        return RuleApi(self._auth).stop_run(data)

    def list_jobs(
        self,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[JobOutput]:
        """

        :param search: A text to filter jobs we are looking for
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return: A paged response that contains a list of JobOutput instances.
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return JobApi(self._auth).list_jobs(project, workspace, search, page_index, page_size)

    def create_job(
        self, data: JobInput, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> JobOutput:
        """
        Create a job

        :param job: A job description (json)
        :return: A JobOutput instance
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return JobApi(self._auth).create_job(project, workspace, data)

    def update_job(self, data: JobOutput, project: Optional[Reference] = None, workspace: Optional[Reference] = None):
        """
        Update a job

        :param job: A job description (json)
        :return: The json structure
        """
        return JobApi(self._auth).update_job(project, workspace, data)

    def list_runs(
        self,
        job: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[RunOutput]:
        """
        List runs of a specific job.

        :param job_id: The identifier of the job
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return: a list of RunOutput
        """
        result = RunApi(self._auth).list_runs(job, project, workspace, search, page_index, page_size)
        return result

    def create_run(
        self,
        data: RunInput,
        job: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> RunOutput:
        """
        Create a run

        :param job: The reference of the job
        :param workspace:
        :param project:
        :param data: A run description (json)
        :param auto_code:
        :return: The json structure
        """
        if isinstance(job, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return RunApi(self._auth).create_run(data, job, project, workspace)

    def get_run(
        self,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> RunOutput:
        if isinstance(job, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return RunApi(self._auth).get_run(run, job, project, workspace)

    def list_artifacts(
        self,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> PagedResponse[ArtifactOutput]:
        if isinstance(job, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return ArtifactApi(self._auth).list_artifacts(run, job, project, workspace)

    def update_run(self, data: RunOutput):
        """
        Update a run

        :param job_id: The identifier of the job
        :param run_id:
        :param run:
        :return: The json structure
        """
        if data.id is None:
            raise ValueError("the id is required")
        return RunApi(self._auth).update_run(data)

    def delete_run(
        self,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        return RunApi(self._auth).delete_run(run, job, project, workspace)

    def create_run_properties(
        self,
        run: Reference,
        properties: List[PropertyInput],
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> RunOutput:
        """
        Create run properties
        :param job:
        :param run:
        :param properties:
        :param project:
        :param workspace:
        :return:
        """
        if isinstance(job, str) and isinstance(run, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return RunApi(self._auth).create_run_properties(run, properties, job, project, workspace)

    def list_run_properties(
        self,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[PropertyOutput]:
        """
        List dataset version properties
        :param job:
        :param run:
        :param project:
        :param workspace:
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return:
        """
        if isinstance(job, str) and isinstance(run, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return RunApi(self._auth).list_run_properties(
            run,
            job,
            project,
            workspace,
            page_index,
            page_size,
        )

    def create_artifact(
        self,
        data: ArtifactInput,
        run: Reference,
        job: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create artifact

        :param job_id: The identifier of the job
        :param run_id:
        :param artifact:
        :return: The json structure
        """
        return ArtifactApi(self._auth).create_artifact(data, run, job, project, workspace)

    def update_artifact(self, artifact: ArtifactOutput):
        """
        Update artifact

        :param job_id: The identifier of the job
        :param run_id:
        :param artifact_id:
        :param artifact:
        :return: The json structure
        """
        return ArtifactApi(self._auth).update_artifact(artifact)

    def get_dataset(
        self, dataset: Reference, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> DatasetOutput:
        """
        List datasets

        :param dataset: The dataset name or id
        :param project:
        :param workspace:

        :return: The json structure
        """
        if isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetApi(self._auth).get_dataset(dataset, project, workspace)

    def list_datasets(
        self,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: str = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[DatasetOutput]:
        """
        List datasets

        :param search: a text used to filter list of datasets
        :param page_index: The index of the page
        :param page_size: The size of the page
        :param project:
        :param workspace:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return DatasetApi(self._auth).list_datasets(project, workspace, search, page_index, page_size)

    def create_dataset(
        self, data: DatasetInput, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> DatasetOutput:
        """
        Create a dataset

        :param data:
        :param project:
        :param workspace:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return DatasetApi(self._auth).create_dataset(data, project, workspace)

    def update_dataset(
        self,
        data: DatasetOutput,
        dataset: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetOutput:
        """
        Update a dataset

        :param dataset:
        :param dataset_object:
        :param project:
        :param workspace:

        :return: The json structure
        """
        if isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetApi(self._auth).update_dataset(data, dataset, project, workspace)

    def delete_dataset(
        self, dataset: Reference, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ) -> None:
        """
        Delete a dataset

        :param dataset: The dataset name or id
        :param project:
        :param workspace:

        :return: The json structure
        """
        if isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        DatasetApi(self._auth).delete_dataset(dataset, project, workspace)

    def get_model(
        self,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Gets a model

        :param model: The model name or id
        :return: The json structure
        """
        if isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelApi(self._auth).get_model(model, project, workspace)

    def list_models(
        self,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[ModelOutput]:
        """
        List models

        :param project: The project name or id
        :param workspace: The workspace name or id
        :param search: The name to search
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return ModelApi(self._auth).list_models(project, workspace, search, page_index, page_size)

    def create_model(
        self, data: ModelInput, project: Optional[Reference] = None, workspace: Optional[Reference] = None
    ):
        """
        Create a model

        :param model:
        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        output = ModelApi(self._auth).create_model(data, project, workspace)
        return output

    def update_model(
        self,
        data: ModelInput,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Update a model

        :param model: The model name or id
        :param model_object: The model json object
        :param project:The project name or id
        :param workspace: The workspace name or id
        :return: The json structure
        """
        if isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelApi(self._auth).update_model(data, model, project, workspace)

    def delete_model(
        self,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        return ModelApi(self._auth).delete_model(model, project, workspace)

    def list_dataset_versions(
        self,
        dataset: Reference,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> PagedResponse[DatasetVersionOutput]:
        """
        List dataset versions

        :param dataset:
        :param search:
        :param page_index: The index of the page
        :param page_size: The size of the page
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).list_dataset_versions(
            dataset, workspace, project, search, page_index, page_size
        )

    def create_dataset_version(
        self,
        data: DatasetVersionInput,
        dataset: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetVersionOutput:
        """
        Create a dataset version

        :param data:
        :param dataset:
        :param project:
        :param workspace:

        :return: The json structure
        """
        if isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).create_dataset_version(data, dataset, project, workspace)

    def update_dataset_version(
        self,
        data: DatasetVersionOutput,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> DatasetVersionOutput:
        """
        Update a dataset version

        :param data:
        :param version:
        :param dataset_version:
        :param project:
        :param workspace:

        :return: The json structure
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).update_dataset_version(data, version, dataset, project, workspace)

    def get_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> Optional[DatasetVersionOutput]:
        """
        Get a dataset version

        :param dataset:
        :param version:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).get_dataset_version(version, dataset, project, workspace)

    def delete_dataset_version(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Delete a dataset version

        :param dataset:
        :param version:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).delete_dataset_version(version, dataset, project, workspace)

    def get_dataset_version_files_metadata(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> List[TreeItem]:
        return DatasetVersionApi(self._auth).get_files_metadata(version, dataset, project, workspace)

    def create_dataset_version_properties(
        self,
        version: Reference,
        properties: Dict[str, Any],
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create data version properties

        :param version:
        :param properties:
        :param dataset:
        :param project:
        :param workspace:
        :return:
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).create_dataset_version_properties(
            version, properties, dataset, project, workspace
        )

    def update_dataset_version_properties(
        self,
        version: Reference,
        property_id: int,
        properties: Dict[str, Any],
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create data version properties

        :param version:
        :param properties:
        :param property_id:
        :param dataset:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).update_dataset_version_properties(
            version, property_id, properties, dataset, project, workspace
        )

    def list_dataset_version_properties(
        self,
        version: Reference,
        dataset: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[PropertyOutput]:
        """
        List dataset version properties

        :param version:
        :param page_index: The index of the page
        :param page_size: The size of the page
        :param dataset:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(dataset, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return DatasetVersionApi(self._auth).list_dataset_version_properties(
            version,
            dataset,
            project,
            workspace,
            page_index,
            page_size,
        )

    def get_model_version(
        self,
        version: Reference,
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> ModelVersionOutput:
        """
        Get a model version

        :param version: The model version name or id
        :param model: The model name or id
        :param project: The project name or id
        :param workspace: The workspace name or id
        """
        if isinstance(version, str) and isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).get_model_version(version, model, project, workspace)

    def list_model_versions(
        self,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[ModelVersionOutput]:
        """
        List model versions

        :param model: The model name or id
        :param project: The project name or id
        :param workspace: The workspace name or id
        :param search: The word to search
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return:
        """
        if isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).list_model_versions(model, project, workspace, search, page_index, page_size)

    def list_model_version_metrics(
        self,
        version: Reference,
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[MetricOutput]:
        """
        List model versions

        :param model: The model name or id
        :param version: The model version name or id
        :param project: The project name or id
        :param workspace: The workspace name or id
        :param search: The word to search
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return:
        """
        if isinstance(version, str) and isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str) and self.workspace is not None:
                if workspace is None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).list_model_version_metrics(
            version,
            model,
            project,
            workspace,
            search,
            page_index,
            page_size,
        )

    def list_model_version_properties(
        self,
        version: Reference,
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[PropertyOutput]:
        """
        List model version properties

        :param model: The model name or id
        :param version: The model version name or id
        :param project: The project name or id
        :param workspace: The workspace name or id
        :param search: The word to search
        :param page_index: The index of the page
        :param page_size: The size of the page
        :return:
        """
        if isinstance(version, str):
            if project is None and self.project is not None:
                project = self.project.id
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return ModelVersionApi(self._auth).list_model_version_properties(
            version, model, project, workspace, search, page_index, page_size
        )

    def create_model_version_properties(
        self,
        version: Reference,
        properties: List[PropertyInput],
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create model version properties

        :param model: The model name or id
        :param version: The model version name or id
        :param properties: The properties object
        :param project: The project name or id
        :param workspace: The workspace name or id
        :return:
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).create_model_version_properties(
            version, properties, model, project, workspace
        )

    def update_model_version_properties(
        self,
        version: Reference,
        property_id: int,
        properties: List[PropertyInput],
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create model version properties

        :param model: The model name or id
        :param version: The model version name or id
        :param property_id : The property id
        :param properties: The properties object
        :param project: The project name or id
        :param workspace: The workspace name or id
        :return:
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).update_model_version_properties(
            version,
            property_id,
            properties,
            model,
            project,
            workspace,
        )

    def create_model_version_metrics(
        self,
        version: Reference,
        metrics: List[MetricInput],
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> None:
        """
        Create model version metrics
        :param model: The model name or id
        :param version: The model version name or id
        :param metrics: The properties object
        :param project: The project name or id
        :param workspace: The workspace name or id
        :return:
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).create_model_version_metrics(version, metrics, model, project, workspace)

    def update_model_version_metrics(
        self,
        model: Reference,
        version: Reference,
        metric_id: int,
        metrics: List[MetricInput],
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Create model version metrics

        :param model: The model name or id
        :param version: The model version name or id
        :param metric_id : The metrics id
        :param metrics: The metrics object
        :param project: The project name or id
        :param workspace: The workspace name or id
        :return:
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).update_model_version_metrics(
            version,
            metric_id,
            metrics,
            model,
            project,
            workspace,
        )

    def create_model_version(
        self,
        data: ModelVersionInput,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> ModelVersionOutput:
        """
        Create a model version

        :param model:
        :param version:
        :param project:
        :param workspace:
        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).create_model_version(data, model, project, workspace)

    def update_model_version(
        self,
        data: ModelVersionInput,
        version: Reference,
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> ModelVersionOutput:
        """
        Update a model version
        :param model:
        :param version:
        :param project:
        :param workspace:
        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return ModelVersionApi(self._auth).update_model_version(data, version, model, project, workspace)

    def delete_model_version(
        self,
        version: Reference,
        model: Optional[Reference] = None,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Delete a dataset version

        :param dataset:
        :param version:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).delete_model_version(version, model, project, workspace)

    def delete_model_version_metrics(
        self,
        version: Reference,
        metric_id: int,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Delete a model version

        :param model:
        :param version:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).delete_model_version_metrics(version, metric_id, model, project, workspace)

    def delete_model_version_properties(
        self,
        version: Reference,
        property_id: int,
        model: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):
        """
        Delete a model version

        :param model:
        :param version:
        :param project:
        :param workspace:

        :return:
        """
        if isinstance(version, str) and isinstance(model, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        return ModelVersionApi(self._auth).delete_model_version_properties(
            version, property_id, model, project, workspace
        )

    def get_attachment(
        self,
        _type: str,
        file_id: int,
        version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ) -> Optional[BinaryIO]:
        """
        Downloads the specified attachment

        :param _type:
        :param version:
        :param file_id:
        :param artifact:
        :param workspace:
        :param project:

        :return: The file requested
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return AttachmentApi(self._auth).get_attachment(_type, file_id, version, artifact, workspace, project)

    def create_attachments(
        self,
        _type: str,
        files: Optional[Sequence[Tuple[str, Tuple[Any, BinaryIO]]]],
        version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ):
        """
        Create an attachment

        :param _type:
        :param version:
        :param artifact:
        :param files:
        :param workspace:
        :param project:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return AttachmentApi(self._auth).post_attachment(_type, version, files, artifact, workspace, project)

    def update_attachments(
        self,
        _type: str,
        files: Sequence[Tuple[str, Tuple[Any, BinaryIO]]],
        version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ):
        """
        Update an attachment

        :param _type:
        :param version:
        :param files:
        :param artifact:
        :param workspace:
        :param project:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return AttachmentApi(self._auth).update_attachments(_type, files, version, artifact, workspace, project)

    def delete_attachment(
        self,
        _type: str,
        version: Reference,
        file_id: int,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ):
        """
        Delete attachment

        :param _type:
        :param version:
        :param file_id:
        :param artifact:
        :param workspace:
        :param project:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return AttachmentApi(self._auth).delete_attachment(_type, version, file_id, artifact, workspace, project)

    def list_attachments(
        self,
        _type: str,
        version: Optional[Reference] = None,
        artifact: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
        project: Optional[Reference] = None,
    ) -> PagedResponse[AttachmentOutput]:
        """
        List attachments

        :param _type:
        :param artifact:
        :param version:
        :param workspace:
        :param project:

        :return: The json structure
        """
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return AttachmentApi(self._auth).list_attachments(_type, version, artifact, workspace, project)

    def get_connection(self, connection: Reference, workspace: Optional[Reference] = None) -> ConnectionOutput:
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if workspace is None:
            raise MissingReferenceError("workspace")
        return ConnectionApi(self._auth).get_connection(connection, workspace)

    def list_connections(
        self,
        workspace: Optional[Reference] = None,
        connection_type: Optional[str] = None,
        search: Optional[str] = None,
        page_index: int = Page.index,
        page_size: int = Page.size,
    ) -> PagedResponse[ConnectionOutput]:
        """
        List connections

        :param workspace:
        :param search:
        :param connection_type:
        :param page_index:
        :param page_size:

        :return: The json structure
        """
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if workspace is None:
            raise MissingReferenceError("workspace")
        return ConnectionApi(self._auth).list_connections(workspace, connection_type, search, page_index, page_size)

    def create_connection(self, data: ConnectionInput, workspace: Optional[Reference] = None) -> ConnectionOutput:
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if workspace is None:
            raise MissingReferenceError("workspace")
        return ConnectionApi(self._auth).create_connection(data, workspace)

    def delete_connection(self, connection: Reference, workspace: Optional[Reference] = None):
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if workspace is None:
            raise MissingReferenceError("workspace")
        return ConnectionApi(self._auth).delete_connection(connection, workspace)

    def update_connection(
        self, data: ConnectionInput, connection: Reference, workspace: Optional[Reference] = None
    ) -> ConnectionOutput:
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        if workspace is None:
            raise MissingReferenceError("workspace")
        return ConnectionApi(self._auth).update_connection(data, connection, workspace)

    def create_code(
        self,
        code_data: CodeInput,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> CodeOutput:
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return CodeApi(self._auth).create_code(code_data, project, workspace)

    def get_code(
        self,
        code: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> CodeOutput:

        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        else:
            raise MissingReferenceError("code", "project")
        if project is None:
            raise MissingReferenceError("project")
        return CodeApi(self._auth).get_code(code, project, workspace)

    def list_codes(
        self,
        project: Reference,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> PagedResponse[CodeOutput]:
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return CodeApi(self._auth).list_codes(project, workspace, search, page_index, page_size)

    def update_code(
        self,
        code_data: CodeOutput,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ):

        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        return CodeApi(self._auth).update_code(code_data, project, workspace)

    def delete_code(
        self,
        code: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> None:
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        CodeApi(self._auth).delete_code(code, project, workspace)

    def create_code_version(
        self,
        code_data: CodeVersionInput,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> CodeVersionOutput:
        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return CodeVersionApi(self._auth).create_code_version(code_data, project, workspace)

    def get_code_version(
        self,
        version: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> CodeVersionOutput:

        if project is None and self.project is not None:
            project = self.project.id
        if workspace is None and self.workspace is not None:
            workspace = self.workspace.id
        return CodeVersionApi(self._auth).get_code_version(version, project, workspace)

    def list_code_versions(
        self,
        project: Reference,
        workspace: Optional[Reference] = None,
        search: Optional[str] = None,
        page_index=Page.index,
        page_size=Page.size,
    ) -> List[CodeVersionOutput]:
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return CodeVersionApi(self._auth).list_code_versions(project, workspace, search, page_index, page_size)

    def update_code_version(
        self,
        code_version_data: CodeVersionInput,
        version: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> CodeVersionOutput:
        if project is None and self.project is not None:
            project = self.project.id
        elif isinstance(project, str):
            if workspace is None and self.workspace is not None:
                workspace = self.workspace.id
        if project is None:
            raise MissingReferenceError("project")
        return CodeVersionApi(self._auth).update_code_version(code_version_data, version, project, workspace)

    def delete_code_version(
        self,
        version: Reference,
        project: Optional[Reference] = None,
        workspace: Optional[Reference] = None,
    ) -> None:
        if isinstance(version, str):
            if project is None and self.project is not None:
                project = self.project.id
            elif isinstance(project, str):
                if workspace is None and self.workspace is not None:
                    workspace = self.workspace.id
        CodeVersionApi(self._auth).delete_code_version(version, project, workspace)
