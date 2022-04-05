from logging import getLogger
from queue import Queue
from typing import Optional
from src.file_syncer.main.base_dir_synchronizer import BaseDirSynchronizer
from src.utils.main.worker_utils import BaseWorker

log = getLogger(__name__)


class DirSynchronizerWorker(BaseWorker):
    """
    A worker that reads from a queue and synchronizes directory changes.
    """

    def __init__(
        self,
        stop_timeout_seconds: Optional[float],
        api: BaseDirSynchronizer,
        queue: Queue,
    ) -> None:
        super().__init__(stop_timeout_seconds)
        self.api = api
        self.queue = queue

    def _run(self) -> None:
        """
        Polls the queue and sends events to the api.
        """
        log.info("Starting directory synchronizer worker.")
        while self.running:
            print("TODO")
