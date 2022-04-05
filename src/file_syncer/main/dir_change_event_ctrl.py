from queue import Queue
from src.file_syncer.main.directory_model import DirectoryChangesModel
from src.file_syncer.main.base_dir_change_event import BaseDirChangeEvent


class DirChangeEventCtrl(BaseDirChangeEvent):
    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def send_event(self, change_event: DirectoryChangesModel) -> None:
        self.queue.put(change_event)
