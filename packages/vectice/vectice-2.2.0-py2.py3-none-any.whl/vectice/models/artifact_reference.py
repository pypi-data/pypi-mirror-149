from typing import Optional

from vectice.api import Reference
from vectice.api.json import ArtifactType, AutoVersionStrategy


class ArtifactReference:
    def __init__(
        self,
        code: Optional[Reference] = None,
        dataset: Optional[Reference] = None,
        model: Optional[Reference] = None,
        version_number: Optional[int] = None,
        version_id: Optional[int] = None,
        version_name: Optional[str] = None,
        version_strategy: Optional[AutoVersionStrategy] = None,
        description: Optional[str] = None,
    ):
        self.dataset = dataset
        self.model = model
        self.code = code
        self.version_number = version_number
        self.version_name = version_name
        self.version_id = version_id
        self.version_strategy = version_strategy
        self.description = description

    @property
    def artifact_type(self) -> ArtifactType:
        if self.dataset is not None:
            return ArtifactType.DATASET
        if self.model is not None:
            return ArtifactType.MODEL
        if self.code is not None:
            return ArtifactType.CODE
        raise RuntimeError("empty artifact")
