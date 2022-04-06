from unittest import TestCase
from unittest.mock import create_autospec
from src.file_syncer.main.dir_reader.base_dir_reader import BaseDirReader
from src.file_syncer.main.dir_reader.dir_reader_worker import DirReaderWorker
from src.file_syncer.main.directory_model import DirectoryModel
from src.file_syncer.main.file_model import FileModel
from src.utils.main.logger_utils import basic_logging
from src.utils.main.queue_utils import EventQueue
from src.utils.main.sleep_utils import sleep_until

basic_logging()
test_loop_delay_seconds = 0.1
two_loops = test_loop_delay_seconds * 2


class WorkerTest(TestCase):
    def test_correct_detects_changes_in_directory(self) -> None:
        empty_dir = DirectoryModel(files=[])
        reader = create_autospec(BaseDirReader)
        reader.read_directory.return_value = empty_dir

        event_sender = create_autospec(EventQueue)

        with DirReaderWorker(
            stop_timeout_seconds=0.5,
            loop_delay_seconds=test_loop_delay_seconds,
            reader=reader,
            event_sender=event_sender,
        ) as w:
            # wait until it gets the initial state of the direcotry
            sleep_until(lambda: len(reader.read_directory.mock_calls) > 0)

            # no files yet
            self.assertEqual(0, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)

            # no changes yet, so not events sent
            event_sender.send.assert_not_called()

            # 1 new file shows up
            new_file_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name.txt", path="name.txt", is_dir=False, contents=""
                    )
                ]
            )
            reader.read_directory.return_value = new_file_dir

            sleep_until(lambda: w.new_file_count == 1)
            self.assertEqual(1, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(0, w.deleted_file_count)
            event_sender.send.assert_any_call(empty_dir.diff(new_file_dir))

            # 1 new file shows up and 1 deleted
            second_file_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name2.txt",
                        path="name2.txt",
                        is_dir=False,
                        contents="name2",
                    )
                ]
            )
            reader.read_directory.return_value = second_file_dir
            sleep_until(lambda: w.deleted_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(0, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)
            event_sender.send.assert_any_call(new_file_dir.diff(second_file_dir))

            # 1 file changed
            changed_file_dir = DirectoryModel(
                files=[
                    FileModel(
                        name="name2.txt",
                        path="name2.txt",
                        is_dir=False,
                        contents="name2 changed",
                    )
                ]
            )
            reader.read_directory.return_value = changed_file_dir
            sleep_until(lambda: w.changed_file_count == 1)
            self.assertEqual(2, w.new_file_count)
            self.assertEqual(1, w.changed_file_count)
            self.assertEqual(1, w.deleted_file_count)
            event_sender.send.assert_any_call(second_file_dir.diff(changed_file_dir))

            self.assertEqual(3, len(event_sender.send.call_args_list))
