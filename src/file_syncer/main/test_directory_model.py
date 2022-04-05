from unittest import TestCase
from src.file_syncer.main.directory_model import DirectoryChangesModel, DirectoryModel
from src.file_syncer.main.file_model import FileModel


class DirectoryModelTest(TestCase):
    def test_directory_with_no_changes(self) -> None:
        first = DirectoryModel(files=[
            FileModel(name="name.txt", path="name.txt", is_dir=False, contents="contents asdf")
        ])
        second = DirectoryModel(files=[])

        self.assertFalse(first.diff(second).changes_detected)
        self.assertEqual(
            DirectoryChangesModel(
                changes_detected=False,
                changed_files=[],
                new_files=[],
                deleted_files=[]
            ),
            first.diff(first)
        )

    def test_directory_with_new_file(self) -> None:
        first = DirectoryModel(files=[])
        second = DirectoryModel(
            files=[
                FileModel(name="name.txt", path="name.txt", is_dir=False, contents="")
            ],
        )
        third = DirectoryModel(
            files=[
                FileModel(name="name.txt", path="name.txt", is_dir=False, contents=""),
                FileModel(
                    name="name2.txt", path="name2.txt", is_dir=False, contents=""
                ),
            ],
        )

        self.assertEqual(
            DirectoryChangesModel(
                changes_detected=True,
                changed_files=[],
                new_files=second.files,
                deleted_files=[]
            ),
            first.diff(second)
        )

        diff = first.diff(third)
        # sort to ensure the same order
        diff.new_files.sort(key=lambda f: f.name)
        self.assertEqual(third.files, diff.new_files)
