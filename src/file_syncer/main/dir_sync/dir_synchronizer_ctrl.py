from logging import getLogger
import os
from src.file_syncer.main.base_dir_synchronizer import BaseDirSynchronizer
from typing import List
from src.file_syncer.main.directory_model import DirectoryChangesModel

log = getLogger(__name__)


class DirSynchronizerCtrl(BaseDirSynchronizer):

    _changes: List[DirectoryChangesModel] = []

    def __init__(self, dst_dir: str) -> None:
        self.dir = dst_dir

    def sync(self, changes: DirectoryChangesModel) -> None:
        """
        Synchronize a set of directory changes to some other directory.
        """
        if not changes.changes_detected:
            return

        self._changes.append(changes)

        # deleted files
        for file in changes.deleted_files:
            full_path = os.path.join(self.dir, file.path)
            log.info("Synchronizing delete %s", file.path)
            if file.is_dir:
                os.rmdir(full_path)
            else:
                os.remove(full_path)

        # new and changed files
        for file in changes.new_files + changes.changed_files:
            full_path = os.path.join(self.dir, file.path)
            log.info("Synchronizing change %s", file.path)
            if file.is_dir:
                os.mkdir(full_path)
            else:
                with open(full_path, "w+") as f:
                    f.write(file.contents)

    def list_changes(self) -> List[DirectoryChangesModel]:
        return self._changes
