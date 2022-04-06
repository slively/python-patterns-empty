import os
from pathlib import Path
from unittest import TestCase
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.file_model import FileModel
from src.file_syncer.tests.test_utils import runIfFileSystem
from src.utils.main.file_utils import clean_and_remake_dir
from src.utils.main.logger_utils import basic_logging

basic_logging()


@runIfFileSystem()
class DirReaderCtrlTest(TestCase):

    tmp_dir = test_working_dir = os.path.join(
        os.getcwd(), "src", "file_syncer", "tests", "tmp"
    )

    def setUp(self) -> None:
        clean_and_remake_dir(self.test_working_dir)

    def _write_file(self, path: str, contents: str) -> None:
        # path relative in tmp dir
        full_path = os.path.join(self.tmp_dir, path)

        # make parent dirs
        os.makedirs(Path(full_path).parent, exist_ok=True)

        # write content
        with open(full_path, "w+") as f:
            f.write(contents)

    def test_correct_detects_changes_in_directory(self) -> None:
        ctrl = DirReaderCtrl(self.tmp_dir)

        # no files yet
        self.assertEqual(0, len(ctrl.read_directory().files))

        # add a file and a dir with a file
        first_contents = "first file contents"
        second_contents = "second file contents"
        self._write_file("first.txt", first_contents)
        self._write_file("child/second.txt", second_contents)

        # 2 files and a folder
        files = ctrl.read_directory().files
        self.assertEqual(3, len(files))
        self.assertEqual(
            FileModel(
                name="first.txt",
                path="first.txt",
                contents=first_contents,
                is_dir=False,
            ),
            files[0],
        )
        self.assertEqual(
            FileModel(
                name="child",
                path="child",
                contents="",
                is_dir=True,
            ),
            files[1],
        )
        self.assertEqual(
            FileModel(
                name="second.txt",
                path=os.path.join("child", "second.txt"),
                contents=second_contents,
                is_dir=False,
            ),
            files[2],
        )

    def test_reset_deletes_and_remakes_dir(self) -> None:
        ctrl = DirReaderCtrl(self.tmp_dir)

        self._write_file("nothing.txt", "")

        # file was created
        self.assertEqual(1, len(ctrl.read_directory().files))

        ctrl.reset()

        # file is gone
        self.assertEqual(0, len(ctrl.read_directory().files))
