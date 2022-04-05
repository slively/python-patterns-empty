from logging import getLogger
from time import sleep
from typing import Optional
from src.file_syncer.main.base_change_event_sender import BaseChangeEventSender

from src.file_syncer.main.base_dir_reader import BaseDirReader
from src.file_syncer.main.directory_model import DirectoryModel
from src.utils.main.statsd_utils import statsd
from src.utils.main.worker_utils import BaseWorker

log = getLogger(__name__)


class DirReaderWorker(BaseWorker):
    """
    A worker that continuously checks the DirReaderApi to detect new files or file changes.
    """

    _current_directory_model: DirectoryModel
    new_file_count = 0
    deleted_file_count = 0
    changed_file_count = 0

    def __init__(
        self,
        stop_timeout_seconds: Optional[float],
        loop_delay_seconds: float,
        reader: BaseDirReader,
        event_sender: BaseChangeEventSender
    ) -> None:
        super().__init__(stop_timeout_seconds)
        self.loop_delay_seconds = loop_delay_seconds
        self.reader = reader
        self.event_sender = event_sender

    def _run(self) -> None:
        """
        Polls the DirReaderApi in a loop while tracking and logging any changes.
        """
        log.info("Starting directory watcher.")
        
        # Initialize state of the directory
        self._current_directory_model = self.reader.read_directory()

        # Main Loop
        while self.running:
            sleep(self.loop_delay_seconds)
            new_directory_model = self.reader.read_directory()
            changes = self._current_directory_model.diff(new_directory_model)
            self._current_directory_model = new_directory_model

            if changes.changes_detected:
                if len(changes.deleted_files) > 0:
                    self.deleted_file_count += 1
                    log.info(
                        "Files deleted: %s",
                        ", ".join(map(lambda f: str(f), changes.deleted_files)),
                    )

                if len(changes.new_files) > 0:
                    self.new_file_count += 1
                    log.info(
                        "Files created: %s",
                        ", ".join(map(lambda f: str(f), changes.new_files)),
                    )

                if len(changes.changed_files) > 0:
                    self.changed_file_count += 1
                    log.info(
                        "Files changed: %s",
                        ", ".join(map(lambda f: str(f), changes.changed_files)),
                    )

                self.event_sender.send_event(changes)
            else:
                log.info("No changes detected.")

            statsd.gauge("new_file_count", self.new_file_count)
            statsd.gauge("changed_file_count", self.changed_file_count)
            statsd.gauge("deleted_file_count", self.deleted_file_count)
