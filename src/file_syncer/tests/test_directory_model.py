
from unittest import TestCase
from src.file_syncer.main.directory_model import DirectoryModel, DirectoryChangesModel
from src.file_syncer.main.file_model import FileModel


class DirectoryModelTest(TestCase):
    def test_directory_with_no_changes(self) -> None:
        simple_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name.txt", path="name.txt", is_dir=False, contents=""
                    )
                ]
            )
        same_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name.txt", path="name.txt", is_dir=False, contents=""
                    )
                ]
            )

        dir_no_changes = DirectoryChangesModel(
                changes_detected=False,
                new_files=[],
                deleted_files=[],
                changed_files=[]
        )
        self.assertEqual(dir_no_changes, simple_dir.diff(same_dir))

    def test_directory_with_new_file(self) -> None:
        simple_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name.txt", path="name.txt", is_dir=False, contents=""
                    )
                ]
            )
        new_file_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name.txt", path="name.txt", is_dir=False, contents=""
                    ),
                    FileModel(
                        name="name2.txt", path="name2.txt", is_dir=False, contents=""
                    )
                ]
            )

        dir_with_new_files = DirectoryChangesModel(
                changes_detected=True,
                new_files=[FileModel(
                        name="name2.txt", path="name2.txt", is_dir=False, contents=""
                    )],
                deleted_files=[],
                changed_files=[]
        )

        self.assertEqual(dir_with_new_files, simple_dir.diff(new_file_dir))
