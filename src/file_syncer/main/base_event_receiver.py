from posixpath import abspath
from src.file_syncer.main.directory_model import DirectoryChangesModel
from abc import abstractmethod


class BaseChangeEventReceiver():
    """
    A simple interface for reading directory change events.
    Default implementation is a no-op.
    """
    @abstractmethod
    def receive(self) -> DirectoryChangesModel:
        pass
