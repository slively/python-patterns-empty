from src.file_syncer.main.directory_model import DirectoryChangesModel


class DirChangeEventApi:
    """
    A simple interface for sending directory change events.
    Default implementation is a no-op.
    """

    def send_event(self, event: DirectoryChangesModel) -> None:
        pass
