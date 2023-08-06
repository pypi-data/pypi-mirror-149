from __future__ import annotations

from typing import Optional

# import logging

from .artifact import Artifact
from .dataset_metadata import DatasetMetadata


class DatasetMetadataArtifact(Artifact):
    """ """

    def __init__(self, dataset: DatasetMetadata, description: Optional[str] = None):
        self.description = description
        self.dataset: DatasetMetadata = dataset

    # @classmethod
    # def create_bigquery(cls, uri: str, description: Optional[str] = None) -> Optional[DatasetMetadataArtifact]:
    #     """ """
    #     dataset_metadata_artifact = DatasetMetadata.create_bigquery(uri)
    #     if dataset_metadata_artifact is not None:
    #         return Artifact(dataset_metadata_artifact, description)
    #     else:
    #         logging.warning("Failed to create metadata based dataset")
    #         return None
    #
    # @classmethod
    # def create_gcs(
    #     cls, uri: Union[str, List[str]], description: Optional[str] = None
    # ) -> Optional[DatasetMetadataArtifact]:
    #     """ """
    #     dataset_metadata_artifact = DatasetMetadata.create_gcs(uri)
    #     if dataset_metadata_artifact is not None:
    #         return cls(dataset_metadata_artifact, description)
    #     else:
    #         logging.warning("Failed to create metadata based dataset")
    #         return None
