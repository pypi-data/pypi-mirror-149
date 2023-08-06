from __future__ import annotations

import logging
import os
from datetime import datetime
from typing import Optional, Union, Dict, List, TYPE_CHECKING, BinaryIO, Any

from vectice.api.json import ModelVersionStatus, PropertyInput, ArtifactVersion, UserDeclaredVersion
from vectice.api.json.metric import create_metrics_input, MetricInput
from vectice.api.json.property import create_properties_input
from vectice.models.property import Property

if TYPE_CHECKING:
    from vectice import Reference
    from vectice.models import Metric, Model
    from vectice.api.client import Client


class ModelVersion:
    """
    A version of the model.

    A ModelVersion store several information that can change between 2 versions like hyper parameters or metrics.

    Noteworthy:
    1. id: Backend will return id if it doesn't exist so it should be optional. SDK doesn't assign id unless we retrieve or reuse a modelVersion.
    2. model: We need the model name or id for a scenario where we won't have the modelVersionId. Currently not in the backend modelVersion.createDTO.
    3. version: Optional as we don't always need it e.g creation of model version. Currently not in the backend modelVersion.createDTO.
    4. status: Backend will throw an error if there's no status, default to EXPERIMENTATION.
    """

    def __init__(
        self,
        model: Model,
        id: int,
        name: str,
        version_number: int,
        description: Optional[str] = None,
        metrics: Optional[Dict[str, float]] = None,
        hyper_parameters: Optional[Dict[str, str]] = None,
        algorithm_name: Optional[str] = None,
        status: ModelVersionStatus = ModelVersionStatus.EXPERIMENTATION,
        resources: Optional[Union[str, List[str]]] = None,
        is_starred: bool = False,
        user_declared_version: Optional[UserDeclaredVersion] = None,
        created_date: datetime = datetime.now(),
        updated_date: Optional[datetime] = None,
        deleted_date: Optional[datetime] = None,
    ):
        """
        :param id: the model version identifier
        :param model: the model name or id that this version is referring
        :param metrics: the list of timestamped key/value pair.
        :param hyper_parameters: list of parameters of the model
        :param version: the version number or versionName of the model
        :param algorithm_name:the algorithm name
        :param status: the status of the version
        :param is_starred: if the model isStarred
        :param resources: Resources to attach to the model version e.g AWS S3 or local files
        """
        self._id = id
        self._model: Model = model
        self._metrics = metrics
        self._properties = hyper_parameters
        self._description = description
        self._algorithmName = algorithm_name
        self._status = status
        self._resources = resources
        self._isStarred = is_starred
        self._name = name
        self._version_number = version_number
        self._created_date = created_date
        self._updated_date = updated_date
        self._deleted_date = deleted_date
        self._user_declared_version: Optional[UserDeclaredVersion] = user_declared_version
        self._client: Client = model._client

    def __repr__(self):
        return f"ModelVersion(model={self.model}, id={self.id}, description={self.description}, metrics={self.metrics}, hyper_parameters={self.properties}, algorithm_name={self.algorithmName}, status={self.status}, resources={self.resources}, is_starred={self.is_starred}, version={self.version}, user_declared_version={self.user_declared_version})"

    @property
    def is_starred(self) -> bool:
        return self._isStarred

    @property
    def model(self) -> Model:
        return self._model

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def metrics(self) -> Optional[Dict[str, float]]:
        return self._metrics

    @property
    def properties(self) -> Optional[Dict[str, str]]:
        return self._properties

    @property
    def description(self) -> Optional[str]:
        return self._description

    @property
    def user_declared_version(self):
        return self._user_declared_version

    @user_declared_version.setter
    def user_declared_version(self, version: UserDeclaredVersion):
        """
        user generated version uses an empty UserDeclaredVersion()
        """
        self._user_declared_version = version

    @property
    def algorithmName(self) -> Optional[str]:
        return self._algorithmName

    @property
    def status(self) -> Optional[ModelVersionStatus]:
        return self._status

    @status.setter
    def status(self, status: ModelVersionStatus):
        self._status = status

    @property
    def resources(self) -> Optional[Union[str, List[str]]]:
        return self._resources

    @resources.setter
    def resources(self, resources):
        self._resources = resources

    @property
    def parent_name(self) -> Optional[str]:
        return self._model.name

    @property
    def parent_id(self) -> Optional[int]:
        return self._model.id

    @property
    def version(self) -> ArtifactVersion:
        return ArtifactVersion(self._version_number, self._name, self._id)

    @property
    def version_number(self) -> int:
        return self._version_number

    @property
    def created_date(self) -> datetime:
        return self._created_date

    def create_metrics(self, metrics: Union[List[Metric], Dict[str, Any]]) -> None:
        """
        Create some metrics to the existing list of metrics.

        There are 2 solution to add metrics:
        - a list of already timestamped metrics.
        - a dictionary of key/value. In this case, the timestamp used is the time this method is called.

        :since:3.0.0

        :param metrics: The metrics e.g metric_key: value = {'metric_key': 1}
        :param version: The name or id of the model version

        :return: None
        """
        if isinstance(metrics, List):
            param = [MetricInput(item.key, item.value, item.timestamp) for item in metrics]
        else:
            param = create_metrics_input(metrics)
        return self._client.create_model_version_metrics(self.id, param)

    def list_metrics(
        self,
        search: Optional[str] = None,
        page_index: int = 1,
        page_size: int = 20,
    ) -> Optional[Dict[str, Any]]:
        """
        List the model version metrics.

        Lists the metrics used for the specified model version.

        :since:3.0.0

        :param version: The name or id of the model version
        :param search: The name to search
        :param page_index:
        :param page_size:

        :return: A List of Metrics
        """
        return {
            prop.key: prop.value
            for prop in self._client.list_model_version_metrics(
                self.id, search=search, page_size=page_size, page_index=page_index
            ).list
        }

    def delete_metrics(
        self,
        metrics: Optional[Union[List[int], List[str]]] = None,
        version: Optional[Reference] = None,
    ) -> None:
        """
        Delete a model version metric.

        Deletes a metric used for the specified model version.

        :new_feature:

        :param metrics: The metric ids or keys
        :param version: The name or id of the model version

        :return: None
        """
        pass

    def create_hyper_parameters(self, hyper_parameters: Dict[str, Union[int, float, str]]):
        """
        Update a model version hyper parameters.

        Updates the hyper parameters used for the specified model version.

        :since:3.0.0

        :param hyper_parameters: The hyper_parameter ids or keys
        :param version: The name or id of the model version

        :return: None
        """
        self._client.create_model_version_properties(self.id, create_properties_input(hyper_parameters))

    def update_hyper_parameters(self, hyper_parameters: Dict[str, Union[str, float, int]]) -> None:
        """
        Update a model version hyper parameters.

        Updates the hyper parameters used for the specified model version.

        :since:3.0.0

        :param hyper_parameters: The hyper_parameter ids or keys
        :param version: The name or id of the model version

        :return: None
        """
        properties = {prop.name: prop.id for prop in self._client.list_model_version_properties(self.id).list}
        for key, value in hyper_parameters.items():
            if properties.get(key):
                property_id = properties[key]
                property_values = Property(key, value)
                try:
                    self._client.update_model_version_properties(
                        self.id, property_id, [PropertyInput(property_values.key, property_values.value)]
                    )
                except Exception as e:
                    logging.warning(f"Hyper Parameter {key} failed to update due to {e}")

    def delete_hyper_parameters(
        self,
        hyper_parameters: Union[List[str], List[int]],
        version: Optional[Reference] = None,
    ) -> None:
        """
        Delete the model version hyper parameters

        Deletes the hyper parameters used for the specified model.

        :new_feature:

        :param hyper_parameters: The hyper_parameter ids or keys
        :param version: The name or id of the model version

        :return: None
        """
        pass

    def list_hyper_parameters(self) -> Dict[str, Any]:
        """
        List the model version hyper parameters.

        :since:3.0.0

        :param version: The name or id of the model version

        :return: A List of Properties
        """
        return {prop.key: prop.value for prop in self._client.list_model_version_properties(self.id).list}

    def update_metrics(
        self,
        metrics: Union[List[Dict[str, int]], Dict[int, int]],
        version: Optional[Reference] = None,
    ) -> None:
        """
        Update a model version metrics

        Update the metrics used for the specified model version

        :since:3.0.0

        :param metrics: The metrics e.g metric_key: value = {'metric_key': 1} OR metric_id: value = {12: 32}
        :param version: The model version name or id

        :return: None
        """
        pass

    def attach_model_files(self, model_object: BinaryIO) -> None:
        """
        Save a model as an object.
        Saves the specified model as an object to be reused.
        :new_feature:
        :param model_object: The model to save
        :param version: The model version name or id
        :return: None
        """
        attachment = [("file", (model_object.name, model_object))]
        self._client.create_attachments("modelversion", attachment, self.id)

    def get_attachment(self, file_path: Union[str, List[str]]) -> Optional[BinaryIO]:
        """
        Get an attachment from the entity

        :new_feature:

        :param file_path: the path to the file

        :return: None
        """
        attachments: List[str] = []
        if isinstance(file_path, str):
            attachments.append(file_path)
        else:
            attachments = file_path

        try:
            attachment_list = {
                attach.fileName: attach.fileId for attach in self._client.list_attachments("modelversion", self.id).list
            }
        except Exception as e:
            raise ValueError(f"ModelVersion attachment failed to retrieve. Due to {e}")
        for file in attachments:
            file_id = attachment_list.get(file)
            if file_id:
                return self._client.get_attachment("modelversion", file_id, self.id)
            else:
                raise ValueError(f"Failed to get attachment named '{file}'. Please check the filename.")
        return None

    def add_attachments(self, file_path: Union[str, List[str]]) -> None:
        """
        Add an attachment to the entity

        :new_feature:

        :param file_path: the path to the file to add

        :return: None
        """
        attachments = []
        if isinstance(file_path, list):

            for file in file_path:
                try:
                    if not os.path.exists(file):
                        raise ValueError(f"the file path {file} is not valid. the file does not exist")
                    curr_file = ("file", (file, open(file, "rb")))
                    attachments.append(curr_file)
                except Exception:
                    logging.warning(f"Did not read {file}.")
        else:
            if not os.path.exists(file_path):
                raise ValueError(f"the file path {file_path} is not valid. the file does not exist")
            attachments = [("file", (file_path, open(file_path, "rb")))]
        self._client.create_attachments("modelversion", attachments, self.id)

    def delete_attachment(self, file_path: Union[str, List[str]]) -> None:
        """
        Delete an attachment from the entity

        :new_feature:

        :param file_path: the path to the file to add

        :return: None
        """
        attachments: List[str] = []
        if isinstance(file_path, str):
            attachments.append(file_path)
        else:
            attachments = file_path

        try:
            attachment_list = {
                attach.fileName: attach.fileId for attach in self._client.list_attachments("modelversion", self.id).list
            }
        except Exception as e:
            raise ValueError(f"ModelVersion attachment failed to retrieve. Due to {e}")

        for file in attachments:
            file_id = attachment_list.get(file)
            if file_id:
                self._client.delete_attachment("modelversion", self.id, file_id)

    def list_attachments(self) -> List[str]:
        """
        List attachments of the entity

        """
        attachments = self._client.list_attachments("modelversion", self.id)
        files = []
        for attachement in attachments.list:
            files.append(attachement.fileName)
        return files

    def update_attachments(self, file_path: Union[str, List[str]]):
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
        self._client.update_attachments("modelversion", attachments, self.id)
