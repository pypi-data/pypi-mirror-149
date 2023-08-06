from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Any

# class ArtifactLocation(TypedDict):

class BaseArtifactStore(ABC):
    @abstractmethod
    def has_artifact(self, name: str, input_hash: str) -> bool: ...
    
    @abstractmethod
    def get_artifact_location(self, name, input_hash) -> Any: ...
    
    @abstractmethod
    def store_artifact_file(self, file_path, artifact_name, input_hash, file_name: str = None) -> Any: ...
    
    @abstractmethod
    def store_artifact_fileobj(self, fileobj, artifact_name, input_hash, file_name: str = None) -> Any: ...

    @abstractmethod
    def get_artifact_fileobj(self, artifact_name: str, input_hash: str) -> BufferedReader: ...
