from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional, Dict, List, Union, BinaryIO, TYPE_CHECKING

from vectice.api import Page, Reference, Client
from vectice.api.json import ModelType, ModelVersionInput, ModelVersionStatus, UserDeclaredVersion, ArtifactVersion
from vectice.api.json.metric import create_metrics_input
from vectice.api.json.property import PropertyInput, create_properties_input
from .model_version import ModelVersion
from .property import create_properties

if TYPE_CHECKING:
    from vectice.models import Project


class Model:
    """
    describe a model

    Noteworthy:
    1. id: Backend will return id if it doesn't exist so it should be optional. SDK doesn't assign id unless we retrieve or resuse a model

    """

    def __init__(
        self,
        name: str,
        id: int,
        project: Project,
        description: Optional[str] = None,
        type: Optional[ModelType] = None,
    ):
        """
        :param name: the name of the model
        :param id: the model id
        :param project: the project this model belongs to
        :param description: the quick description of the model
        :param type: type of the model
        """
        self._id = id
        self._project = project
        self._name = name
        self._type = type
        self._description = description
        self._client: Client = project._client

    def __repr__(self):
        return f"Model(name={self.name}, id={self.id}, description={self.description}, type={self._type})"

    @property
    def id(self) -> int:
        """
        Model identifier
        :return:
        """
        return self._id

    @property
    def project(self) -> Project:
        """
        The project this model belong to
        """
        return self._project

    @property
    def name(self) -> str:
        """
        Name of the model
        """
        return self._name

    @property
    def description(self) -> Optional[str]:
        """
        Quick description of the model
        """
        return self._description

    @property
    def type(self) -> Optional[ModelType]:
        """
        Type of the model
        """
        return self._type

    def __eq__(self, o: object) -> bool:
        return (
            isinstance(o, Model)
            and self.id == o.id
            and self.name == o.name
            and o.description == self.description
            and self.type == o.type
        )

    def create_model_version(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: ModelVersionStatus = ModelVersionStatus.EXPERIMENTATION,
        algorithm_name: Optional[str] = None,
        is_starred: Optional[bool] = False,
        metrics: Optional[Dict] = None,
        hyper_parameters: Optional[Dict] = None,
        version: Optional[ArtifactVersion] = None,
        user_declared_version: Optional[UserDeclaredVersion] = None,
        resources: Optional[Union[Union[str, BinaryIO], List[Union[str, BinaryIO]]]] = None,
    ) -> ModelVersion:
        """
        Create a new model version.

        Creates a new model version with all the existing params in Vectice.

        :param version: The model version name or id
        :param name: The name of the model version
        :param description: The description of the model
        :param status: The status of the model e.g 'OTHER'/'CLASSIFICATION'/'REGRESSION'
        :param algorithm_name: The algorithm the model version uses
        :param is_starred: Whether the model is starred or not
        :param metrics: The model version metrics
        :param hyper_parameters: The model version hyper parameters
        :param user_declared_version:
        :param resources: Resources to attach to the model version e.g AWS S3 or local files

        :return: A ModelVersion
        """
        data = ModelVersionInput(
            name=name,
            description=description,
            repository=resources,
            algorithmName=algorithm_name,
            status=status.value,
            isStarred=is_starred,
        )
        model_version_output = self._client.create_model_version(data, self._id)
        if hyper_parameters:
            self._client.create_model_version_properties(
                model_version_output.id, create_properties_input(hyper_parameters)
            )
        if metrics:
            self._client.create_model_version_metrics(model_version_output.id, create_metrics_input(metrics))

        return ModelVersion(
            self,
            model_version_output.id,
            model_version_output.name,
            model_version_output.version_number,
            model_version_output.description,
            metrics,
            hyper_parameters,
            model_version_output.algorithm_name,
            model_version_output.status,
            model_version_output.resources,
            model_version_output.is_starred,
            created_date=model_version_output.created_date if model_version_output.created_date else datetime.now(),
            updated_date=model_version_output.updated_date,
            deleted_date=model_version_output.deleted_date,
        )

    def update_model_version(
        self,
        version: Reference,
        name: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = "EXPERIMENTATION",
        algorithm: Optional[str] = None,
        is_starred: Optional[bool] = False,
        metrics: Optional[Dict] = None,
        hyper_parameters: Optional[Dict] = None,
        resources: Optional[Union[str, List[str]]] = None,
    ) -> ModelVersion:
        """
        Update a model version.
        Updates the specified model version with the new params passed to this function.
        :param version: The model version name or id
        :param name: The name of the model version
        :param description: The description of the model
        :param status: The status of the model e.g 'EXPERIMENTATION'/'STAGING'/'PRODUCTION'
        :param algorithm: The algorithm the model version uses
        :param is_starred: Whether the model is starred or not
        :param metrics: The model version metrics
        :param hyper_parameters: The model version hyper parameters
        :param resources: Resources to update to the model version e.g AWS S3 or local files
        :return: None
        """
        model_version_input = ModelVersionInput(
            name=name,
            description=description,
            isStarred=is_starred,
            status=status,
            algorithmName=algorithm,
            metrics=metrics,
            hyper_parameters=hyper_parameters,
            resources=resources,
        )
        model_version_output = self._client.update_model_version(model_version_input, version, self._id)
        if hyper_parameters:
            new_parameters = create_properties(hyper_parameters)
            parameters = {
                prop.key: prop.id
                for prop in self._client.list_model_version_properties(model_version_output.id, self._id).list
            }
            for param in new_parameters:
                if parameters.get(param.key):
                    self._client.update_model_version_properties(
                        model_version_output.id, parameters[param.key], [PropertyInput(param.key, param.value)]
                    )
        if metrics:
            new_metrics = create_metrics_input(metrics)
            metrics_list = {
                metric.key: metric.id
                for metric in self._client.list_model_version_metrics(model_version_output.id, self._id).list
            }
            for metric in new_metrics:
                temp = metrics_list.get(metric.key)
                if temp is not None:
                    self._client.update_model_version_metrics(self.id, model_version_output.id, temp, [metric])
        return ModelVersion(
            self,
            model_version_output.id,
            model_version_output.name,
            model_version_output.version_number,
            model_version_output.description,
            metrics,
            hyper_parameters,
            model_version_output.algorithm_name,
            model_version_output.status,
            model_version_output.resources,
            model_version_output.is_starred,
            model_version_output.user_declared_version,
            model_version_output.created_date if model_version_output.created_date else datetime.now(),
            model_version_output.updated_date,
            model_version_output.deleted_date,
        )

    def list_model_versions(
        self, search: Optional[str] = None, page_index: int = Page.index, page_size: int = Page.size
    ) -> List[ModelVersion]:
        """
        List the model versions of a model.

        Lists all the versions created out of the specified model.

        :param search: The name to search
        :param page_index:
        :param page_size:

        :return: List of ModelVersions\
        """

        def get_parameters(id: int):
            properties_output = self._client.list_model_version_properties(id, self._id)
            parameters = {item.key: item.value for item in properties_output.list}
            return parameters

        model_versions = self._client.list_model_versions(self.id, None, None, search, page_index, page_size)
        return [
            ModelVersion(
                self,
                model_version.id,
                model_version.name,
                model_version.version_number,
                model_version.description,
                model_version.metrics,
                get_parameters(model_version.id),
                model_version.algorithm_name,
                model_version.status,
                None,
                model_version.is_starred,
                model_version.user_declared_version,
                model_version.created_date if model_version.created_date else datetime.now(),
                model_version.updated_date,
                model_version.deleted_date,
            )
            for model_version in model_versions.list
        ]

    def get_model_version(
        self,
        version: Reference,
    ) -> ModelVersion:
        """
        Get a model version.
        Gets a specific version of a model.
        :since:3.0.0
        :param version: The model version name or id
        :return: A ModelVersion
        """
        model_version_output = self._client.get_model_version(version=version, model=self._id)
        properties_output = self._client.list_model_version_properties(model_version_output.id, self.id)
        parameters = {item.key: item.value for item in properties_output.list}
        metrics_output = self._client.list_model_version_metrics(model_version_output.id, self.id)
        metrics = {item.key: item.value for item in metrics_output.list}
        return ModelVersion(
            self,
            model_version_output.id,
            model_version_output.name,
            model_version_output.version_number,
            model_version_output.description,
            metrics,
            parameters,
            model_version_output.algorithm_name,
            model_version_output.status,
            None,
            model_version_output.is_starred,
            model_version_output.user_declared_version,
            model_version_output.created_date if model_version_output.created_date else datetime.now(),
            model_version_output.updated_date,
            model_version_output.deleted_date,
        )

    def delete_model_version(
        self,
        version: Reference,
    ) -> None:
        """
        Delete a model version.
        Deletes the specified version of a model.
        :new_feature:
        :param version: The model version name or id
        :return: None
        """
        self._client.delete_model_version(version, self._id)

    def delete_model_version_properties(self, version: Reference, properties: List[str]):
        property_ids = {item.key: item.id for item in self._client.list_model_version_properties(version, self.id).list}
        for prop in properties:
            if property_ids.get(prop):
                self._client.delete_model_version_properties(version, property_ids[prop], self.id)
            else:
                logging.warning(f"Hyper Parameter {prop} was not be found.")

    def delete_model_version_metrics(self, version: Reference, metrics: List[str]):
        metric_ids = {item.key: item.id for item in self._client.list_model_version_metrics(version, self.id).list}
        for metric in metrics:
            temp = metric_ids.get(metric)
            if temp is not None:
                self._client.delete_model_version_metrics(version, temp, self.id)
            else:
                logging.warning(f"Metric {metric} was not be found.")
