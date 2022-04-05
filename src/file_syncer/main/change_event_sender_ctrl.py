from abc import abstractmethod
from queue import Queue
from src.file_syncer.main.directory_model import DirectoryChangesModel
from src.file_syncer.main.base_change_event_sender import BaseChangeEventSender


class DirChangeEventCtrl(BaseChangeEventSender):

    def __init__(self, queue: Queue) -> None:
        self.queue = queue

    def send_event(self, event: DirectoryChangesModel) -> None:
        self.queue.put(event)
