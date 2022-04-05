from abc import abstractmethod
from typing import List
from src.file_syncer.main.directory_model import DirectoryChangesModel


class BaseDirSynchronizer:
    @abstractmethod
    def sync(self, changes: DirectoryChangesModel) -> None:
        """
        Synchronize a set of directory changes to some other directory.
        """
        raise NotImplementedError

    @abstractmethod
    def list_changes(self) -> List[DirectoryChangesModel]:
        """
        List all changes received so far, will not return events that contain no changes.
        """
        raise NotImplementedError
