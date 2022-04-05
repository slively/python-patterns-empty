from logging import getLogger
from typing import Optional
from src.file_syncer.main.base_dir_synchronizer import BaseDirSynchronizer
from src.file_syncer.main.directory_model import DirectoryChangesModel
from src.utils.main.queue_utils import ReceiveEventQueue
from src.utils.main.worker_utils import BaseWorker

log = getLogger(__name__)


class DirSynchronizerWorker(BaseWorker):
    """
    A worker that reads from a queue and synchronizes directory changes.
    """

    def __init__(
        self,
        stop_timeout_seconds: Optional[float],
        reader: ReceiveEventQueue[DirectoryChangesModel],
        syncer: BaseDirSynchronizer,
    ) -> None:
        super().__init__(stop_timeout_seconds)
        self.reader = reader
        self.syncer = syncer

    def _run(self) -> None:
        """
        Polls the queue and sends events to the api.
        """
        while self.running:
            changes = self.reader.receive()
            log.info("Received changes: %s", str(changes))
            self.syncer.sync(changes)
