import os
from unittest import TestCase
from src.file_syncer.main.simple_main import Worker
from src.utils.main.file_utils import clean_and_remake_dir
from src.utils.main.logger_utils import basic_logging
from src.utils.main.sleep_utils import sleep_until

basic_logging()
test_dir = os.path.join(os.path.dirname(__file__), "tmp")
test_sync_dir = os.path.join(os.path.dirname(__file__), "tmp2")


class TestSimpleWorker(TestCase):
    def setUp(self) -> None:
        clean_and_remake_dir(test_dir)
        clean_and_remake_dir(test_sync_dir)

    def test_correct_detects_changes_in_directory(self) -> None:
        w = Worker(dir=test_dir, sync_dir=test_sync_dir)

        try:
            # not started
            self.assertEqual(0, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)

            w.start()

            # 1 new file shows up with no contents
            first_contents = "contents"
            first_file = os.path.join(test_dir, "name.txt")
            first_synced_file = os.path.join(test_sync_dir, "name.txt")
            with open(first_file, "w+") as f:
                f.write(first_contents)
            sleep_until(lambda: w.new_file_count == 1)
            self.assertEqual(1, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)
            with open(first_synced_file, "r") as f:
                self.assertEqual(first_contents, f.read())

            # 1 new file shows up and 1 deleted
            second_contents = "name2"
            second_file = os.path.join(test_dir, "name2.txt")
            second_synced_file = os.path.join(test_sync_dir, "name2.txt")
            with open(second_file, "w+") as f:
                f.write(second_contents)

            sleep_until(lambda: w.new_file_count == 2)
            os.remove(first_file)
            sleep_until(lambda: w.deleted_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)
            with open(second_synced_file, "r") as f:
                self.assertEqual(second_contents, f.read())

            # 1 file changed
            changed_contents = "name2 changed"
            with open(second_file, "w+") as f:
                f.write(changed_contents)
            sleep_until(lambda: w.changed_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(1, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)
            with open(second_synced_file, "r") as f:
                self.assertEqual(changed_contents, f.read())

        finally:
            w.stop()
