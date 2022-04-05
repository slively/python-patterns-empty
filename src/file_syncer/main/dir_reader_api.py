from abc import abstractmethod
from src.file_syncer.main.directory_model import DirectoryModel


class DirReaderApi:
    """
    Base interface for the directory reader api.
    """

    @abstractmethod
    def read_directory(self) -> DirectoryModel:
        """
        Returns all files within the provided directory.
        """
        raise NotImplementedError

    @abstractmethod
    def reset(self) -> None:
        """
        rm -rf the provided directory then re-create it.
        """
        raise NotImplementedError
