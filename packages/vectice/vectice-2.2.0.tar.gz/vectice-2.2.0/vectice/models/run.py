from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING, Union, Dict

from vectice.api import Client
from vectice.api.json import (
    RunStatus,
    ArtifactType,
    StopRunInput,
    ArtifactVersion,
    ArtifactReferenceInput,
    RulesDatasetVersionInput,
    RulesModelVersionInput,
    RulesCodeVersionInput,
    RunInput,
    JobInput,
    StartRunInput,
)
from .artifact_reference import ArtifactReference
from .git_version import GitVersion
from .integration import AbstractIntegration

if TYPE_CHECKING:
    from vectice.models import Job


def __create_artifact_input__(item: ArtifactReference) -> ArtifactReferenceInput:
    result = ArtifactReferenceInput(item.artifact_type)
    if item.dataset is not None:
        result.dataset = __to_dataset_version_input__(item)
    elif item.model is not None:
        result.model = __to_model_version_input__(item)
    elif item.code is not None:
        result.code = __to_code_version_input__(item)
    return result


def __to_code_version_input__(artifact_reference: ArtifactReference) -> RulesCodeVersionInput:
    result = RulesCodeVersionInput()
    if isinstance(artifact_reference.code, int):
        result.parentId = artifact_reference.code
    else:
        result.parentName = str(artifact_reference.code)
    result.version = ArtifactVersion(version_id=artifact_reference.version_id)
    return result


def __to_dataset_version_input__(artifact_reference: ArtifactReference) -> RulesDatasetVersionInput:
    result = RulesDatasetVersionInput()
    if isinstance(artifact_reference.dataset, int):
        result.parentId = artifact_reference.dataset
    else:
        result.parentName = str(artifact_reference.dataset)
    if artifact_reference.version_id is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_id=artifact_reference.version_id)
        return result
    if artifact_reference.version_name is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_name=artifact_reference.version_name)
        return result
    if artifact_reference.version_number is not None:
        result.autoVersion = False
        result.version = ArtifactVersion(version_number=artifact_reference.version_number)
        return result
    if artifact_reference.version_strategy is not None:
        result.autoVersion = True
        return result
    raise RuntimeError(f"Missing version information for dataset {artifact_reference.dataset}")


def __to_model_version_input__(artifact_reference: ArtifactReference) -> RulesModelVersionInput:
    result = RulesModelVersionInput()
    # result.algorithmName=artifact_reference.algorithmName
    # if artifact_reference.description is not None:
    #    result.description = artifact_reference.description
    # if artifact_reference.metrics is not None:
    #     result.metrics = [
    #         dict(key=k, value=v, timestamp=datetime.now().isoformat()) for k, v in artifact_reference.metrics.items()
    #     ]
    # if artifact_reference.properties is not None:
    #     result.properties = [dict(key=k, value=str(v)) for k, v in artifact_reference.properties.items()]
    if isinstance(artifact_reference.model, int):
        result.parentId = artifact_reference.model
    else:
        result.parentName = str(artifact_reference.model)
    if artifact_reference.version_id is not None:
        result.version = ArtifactVersion(id=artifact_reference.version_id)
        return result
    if artifact_reference.version_name is not None:
        result.version = ArtifactVersion(version_name=artifact_reference.version_name)
        return result
    if artifact_reference.version_number is not None:
        result.version = ArtifactVersion(version_number=artifact_reference.version_number)
        return result
    raise RuntimeError(f"Missing version information for model {artifact_reference.model}")


class Run:
    """
    The Run acts as the ActiveRun, JobRun and Job.
    The run is not viewable in the Vectice platform until the job is started.
    """

    def __init__(
        self,
        id: int,
        job: Job,
        name: str,
        system_name: Optional[str] = "",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        status: RunStatus = RunStatus.SCHEDULED,
        auto_code: bool = False,
        check_remote_repository: bool = True,
        description: Optional[str] = None,
        properties: Optional[Dict[str, str]] = None,
    ):
        """
        :param id:
        :param job:
        :param name:
        :param system_name:
        :param start_date:
        :param end_date:
        :param status:
        :param inputs:
        """
        self._id = id
        self._job = job
        self._name = name
        self._systemName = system_name
        self._description = description
        self._properties = properties
        self._startDate = start_date
        self._endDate = end_date
        self._status = status
        self._duration: Optional[int] = None
        self._client: Client = job._client
        self._integration_client: Optional[AbstractIntegration] = job._integration_client
        self._inputs: List[ArtifactReference] = []
        self._outputs: List[ArtifactReference] = []
        self._auto_code = auto_code
        self._check_remote_repository = check_remote_repository

    def __repr__(self):
        return f"Run(id={self.id}, job={self.job}, name={self.name}, system_name={self.system_name}, start_date={self.start_date}, end_date={self.end_date}, duration={self.duration}, status={self.status}, inputs={self.inputs}, outputs={self.outputs})"

    def __enter__(self) -> Run:
        if self._status == RunStatus.SCHEDULED:
            self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        status = RunStatus.COMPLETED if exc_type is None else RunStatus.FAILED
        try:
            self.end_run(status=status)
        except Exception as e:
            self.fail(reason=str(e))
        finally:
            return exc_type is None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def job(self):
        return self._job

    @job.setter
    def job(self, job):
        self._job = job

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def system_name(self):
        return self._systemName

    @system_name.setter
    def system_name(self, system_name: str):
        self._systemName = system_name

    @property
    def description(self) -> Optional[str]:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def properties(self) -> Optional[Dict]:
        return self._properties

    @properties.setter
    def properties(self, properties: Dict):
        self._properties = properties

    @property
    def start_date(self):
        return self._startDate

    @property
    def end_date(self):
        return self._endDate

    @end_date.setter
    def end_date(self, end_date):
        self._endDate = end_date

    @property
    def status(self) -> RunStatus:
        return self._status

    @status.setter
    def status(self, status: RunStatus):
        self._status = status

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, duration):
        self._duration = duration

    @property
    def inputs(self) -> List[ArtifactReference]:
        return self._inputs

    @property
    def outputs(self) -> List[ArtifactReference]:
        return self._outputs

    def to_reference_input(self, item: ArtifactReference) -> ArtifactReferenceInput:
        return ArtifactReferenceInput(
            item.artifact_type,
            item.description,
            RulesDatasetVersionInput(
                parentName=str(item.dataset) if not isinstance(item.dataset, int) else None,
                parentId=item.dataset if isinstance(item.dataset, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id)
                if item.version_strategy is None
                else None,
                autoVersion=True if item.version_strategy is not None else None,
            )
            if item.artifact_type == ArtifactType.DATASET
            else None,
            RulesModelVersionInput(
                parentName=str(item.model) if not isinstance(item.model, int) else None,
                parentId=item.model if isinstance(item.model, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id),
            )
            if item.artifact_type == ArtifactType.MODEL
            else None,
            RulesCodeVersionInput(
                parentName=str(item.model) if not isinstance(item.model, int) else None,
                parentId=item.model if isinstance(item.model, int) else None,
                version=ArtifactVersion(item.version_number, item.version_name, item.version_id),
            )
            if item.artifact_type == ArtifactType.CODE
            else None,
        )

    def add_output(self, output: ArtifactReference):
        if self._outputs is None:
            self._outputs = [output]
        else:
            self._outputs.append(output)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                outputs=[self.to_reference_input(output)],
            )

    def add_outputs(self, outputs: List[ArtifactReference]):
        if self._outputs is None:
            self._outputs = outputs
        else:
            self._outputs.extend(outputs)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                outputs=[self.to_reference_input(output) for output in outputs],
            )

    def add_input(self, input: ArtifactReference):
        if self._inputs is None:
            self._inputs = [input]
        else:
            self._inputs.append(input)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                inputs=[self.to_reference_input(input)],
            )

    def add_inputs(self, inputs: List[ArtifactReference]):
        if self._inputs is None:
            self._inputs = inputs
        else:
            self._inputs.extend(inputs)
        if self.status != RunStatus.SCHEDULED:
            self._client.fill_run(
                self.id,
                inputs=[self.to_reference_input(input) for input in inputs],
            )

    def start(
        self,
        inputs: Optional[List[ArtifactReference]] = None,
        auto_code: Optional[bool] = None,
        check_remote_repository: Optional[bool] = None,
    ) -> None:
        """
        Start the run.
        :since:1.0.0
        :return: None
        """
        if inputs is not None:
            self.add_inputs(inputs)

        if auto_code is True or (auto_code is None and self._auto_code is True):
            code_artifact_is_present = False
            if self._inputs is not None:
                for artifact in self._inputs:
                    code_artifact_is_present = code_artifact_is_present or artifact.artifact_type == ArtifactType.CODE
            if not code_artifact_is_present:
                git_version = GitVersion.create(
                    check_remote_repository=check_remote_repository
                    if check_remote_repository is not None
                    else self._check_remote_repository
                )
                if git_version:
                    code_version = self.job.project.create_code_version(git_version=git_version)
                    self.add_input(ArtifactReference(code=code_version.code_id, version_id=code_version.id))

        job_input = JobInput(self.job.name, self.job.description, self.job.type)
        self.status = RunStatus.STARTED
        run_input = RunInput(self.name, job_input, self.system_name, self.start_date, self.end_date, self.status)
        if self._inputs is None:
            artifact_inputs = None
        else:
            artifact_inputs = [__create_artifact_input__(artifact) for artifact in self._inputs]
        rule_input = StartRunInput(job_input, run_input, artifact_inputs)
        if self._integration_client:
            try:
                self._integration_client.before_start(self)
            except Exception as e:
                logging.warning(e)
        self._client.start_run(rule_input)
        if self._integration_client:
            try:
                self._integration_client.after_start(self)
            except Exception as e:
                logging.warning(e)

    def end_run(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        status: RunStatus = RunStatus.COMPLETED,
        reason: Optional[str] = None,
    ) -> None:
        """
        End the current (last) active run started by :func:`~Vectice.start_run`.
        To end a specific run, use :func:`~Vectice.stop_run` instead.

        :return: None
        """

        if outputs is not None:
            self.add_outputs(outputs)
        run_output = self._client.get_run(self.id)
        run_output["status"] = status
        run_output["endDate"] = datetime.now()
        run_output["reason"] = reason
        rule_output = StopRunInput(run_output)
        if self._integration_client is not None:
            try:
                self._integration_client.before_stop(self)
            except Exception as e:
                logging.warning(e)
        output = self._client.stop_run(rule_output)
        self._status = output.jobRun.status
        self._duration = output.jobRun.duration
        self._endDate = output.jobRun.end_date
        if self._integration_client is not None:
            try:
                self._integration_client.after_stop(self)
            except Exception as e:
                logging.warning(e)

    def complete(self, outputs: Optional[List[ArtifactReference]] = None) -> None:
        """
        Complete the run.
        :since:1.0.0
        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.COMPLETED)

    def fail(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Fail the run.
        :since:1.0.0
        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.FAILED, reason=reason)

    def abort(
        self,
        outputs: Optional[List[ArtifactReference]] = None,
        reason: Optional[str] = None,
    ) -> None:
        """
        Abort the run.

        The end date of the Run will be set at the time this method is called.

        :since:3.0.0

        :param outputs: list of artifacts
        :param reason: the reason the run is aborted
        :return: None
        """
        self.end_run(outputs=outputs, status=RunStatus.ABORTED, reason=reason)

    def add_attachments(self, file_path: Union[str, List[str]]):
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
        self._client.create_attachments("run", attachments, self.id)

    def list_attachments(self) -> List[str]:
        """
        List attachments of the entity
        """
        attachments = self._client.list_attachments("run", self.id)
        files = []
        for attachement in attachments.list:
            files.append(attachement.fileName)
        return files

    def delete_attachments(self, file_path: Union[List[str], str]):
        """
        remove an attachment from the entity
        :param file_path:
        """
        attachments: List[str] = []
        if isinstance(file_path, str):
            attachments.append(file_path)
        else:
            attachments = file_path

        try:
            attachment_list = {
                attach.fileName: attach.fileId for attach in self._client.list_attachments("run", self.id).list
            }
        except Exception as e:
            raise ValueError(f"DatasetVersion attachment failed to retrieve. Due to {e}")
        for file in attachments:  # type: ignore
            file_id = attachment_list.get(file)
            if file_id:
                self._client.delete_attachment("run", self.id, file_id)

    def clean(self):
        self._outputs = None
        self._inputs = None
        self._endDate = None
        self._duration = None
        self._status = RunStatus.SCHEDULED
