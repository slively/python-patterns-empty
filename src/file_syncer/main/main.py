import argparse
from typing import Any
from src.file_syncer.main.dir_reader.dir_reader_ctrl import DirReaderCtrl
from src.file_syncer.main.dir_reader.dir_reader_worker import DirReaderWorker
from src.file_syncer.main.dir_sync.dir_synchronizer_ctrl import DirSynchronizerCtrl
from src.file_syncer.main.dir_sync.dir_synchronizer_worker import DirSynchronizerWorker
from src.file_syncer.main.directory_model import DirectoryChangesModel
from src.utils.main.logger_utils import forwarded_logging
from src.utils.main.queue_utils import EventQueue

forwarded_logging()


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="Dir synchronizer.")
    parser.add_argument(
        "--dir", help="The root directory for the dir reader api.", required=True
    )
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=True
    )
    parser.add_argument(
        "--stop_timeout",
        help="Number of seconds to wait for workers to exit.",
        default=5.0,
        type=float,
    )
    parser.add_argument(
        "--dir_poll_interval",
        help="Number of seconds to wait while polling for directory changes.",
        default=3.0,
        type=float,
    )
    return parser.parse_args()


def run() -> None:
    args = parse_args()

    # Events
    event_queue = EventQueue[DirectoryChangesModel]()

    # Reader
    dir_reader = DirReaderCtrl(dir=args.dir)
    dir_reader_worker = DirReaderWorker(
        stop_timeout_seconds=args.stop_timeout,
        loop_delay_seconds=0.1,
        reader=dir_reader,
        event_sender=event_queue,
    )

    # Synchronizer
    dir_synchronizer = DirSynchronizerCtrl(dst_dir=args.sync_dir)
    dir_synchronizer_worker = DirSynchronizerWorker(
        stop_timeout_seconds=args.stop_timeout,
        events_receiver=event_queue,
        syncer=dir_synchronizer,
    )

    # Run Workers
    dir_reader_worker.start()
    dir_synchronizer_worker.start()


if __name__ == "__main__":
    run()
