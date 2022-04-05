from src.file_syncer.main.base_dir_synchronizer import BaseDirSynchronizer
from typing import List
from src.file_syncer.main.directory_model import DirectoryChangesModel


class DirSynchronizerCtrl(BaseDirSynchronizer):
    def __init__(self, dst_dir: str) -> None:
        self.dir = dst_dir

    def sync(self, changes: DirectoryChangesModel) -> None:
        """
        Synchronize a set of directory changes to some other directory.
        """
        pass

    def list_changes(self) -> List[DirectoryChangesModel]:
        """
        List all changes received so far, will not return events that contain no changes.
        """
        pass
