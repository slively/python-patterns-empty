from logging import getLogger
from typing import Dict, List
from pydantic import BaseModel

from src.file_syncer.main.file_model import FileModel


log = getLogger(__name__)


class DirectoryChangesModel(BaseModel):
    changes_detected: bool
    new_files: List[FileModel] = []
    deleted_files: List[FileModel] = []
    changed_files: List[FileModel] = []


class DirectoryModel(BaseModel):
    """
    Represents a directory with FileModels in it.
    """

    files: List[FileModel]

    def files_by_path(self) -> Dict[str, FileModel]:
        """
        Convert the list of FileModel to a dictionary of file path to the model.
        """
        return {file.path: file for file in self.files}

    def diff(self, directory: "DirectoryModel") -> DirectoryChangesModel:
        """
        Calculate and return the DirectoryChangesModel from this DirectoryModel to the provided directory.
        """
        this_files_by_path = self.files_by_path()
        this_file_paths = this_files_by_path.keys()

        that_files_by_path = directory.files_by_path()
        that_file_paths = that_files_by_path.keys()

        deleted_file_paths = this_file_paths - that_file_paths
        new_file_paths = that_file_paths - this_file_paths
        existing_file_paths = that_file_paths - new_file_paths
        changed_file_paths = []
        for file_path in existing_file_paths:
            previous_content = this_files_by_path[file_path].contents
            current_content = that_files_by_path[file_path].contents
            if previous_content != current_content:
                changed_file_paths.append(file_path)

        new_files = list(map(lambda path: that_files_by_path[path], new_file_paths))
        changed_files = list(
            map(lambda path: that_files_by_path[path], changed_file_paths)
        )
        deleted_files = list(
            map(lambda path: this_files_by_path[path], deleted_file_paths)
        )

        return DirectoryChangesModel(
            changes_detected=len(changed_file_paths) > 0
            or len(deleted_file_paths) > 0
            or len(new_file_paths) > 0,
            new_files=new_files,
            changed_files=changed_files,
            deleted_files=deleted_files,
        )
