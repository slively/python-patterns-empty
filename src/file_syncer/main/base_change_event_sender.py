from abc import abstractmethod
from src.file_syncer.main.directory_model import DirectoryChangesModel


class BaseChangeEventSender:
    """
    A simple interface for sending directory change events.
    Default implementation is a no-op.
    """

    @abstractmethod
    def send(self, event: DirectoryChangesModel) -> None:
        pass
