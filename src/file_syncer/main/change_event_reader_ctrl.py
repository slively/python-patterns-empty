from src.file_syncer.main.directory_model import DirectoryChangesModel
from src.file_syncer.main.base_event_receiver import BaseChangeEventReceiver
from queue import Queue


class ChangeEventReceiverCtrl(BaseChangeEventReceiver):
    def __init__(self, event_queue: Queue) -> None:
        self.queue = event_queue

    def receive(self) -> DirectoryChangesModel:
        return self.queue.get()
