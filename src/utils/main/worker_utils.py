from abc import abstractmethod
from logging import getLogger
from threading import Thread
from typing import Any, Optional
from typing_extensions import Self  # type:ignore

log = getLogger(__name__)


class BaseWorker:
    """
    A simple base class for a worker that should be launched in a thread and run some continuous main loop.
    Has standard start/stop methods, and implements enter/exit for easier testing using 'with'.
    """

    running = False
    _thread: Optional[Thread] = None

    def __init__(self, stop_timeout_seconds: Optional[float]) -> None:
        """
        stop_timeout_seconds: When set to None (not recommended) calling stop will block indefinitely until the thread
                              exits.
                              Otherwise will wait specified number of seconds for thread to exit before killing it.
        """
        self.stop_timeout_seconds = stop_timeout_seconds

    @abstractmethod
    def _run(self) -> None:
        """
        Meant to be implemented by the inherited class and should run an infinite loop as long as
        self.running is True.
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        Start the worker thread and set running to True.
        Throws if the worker is already running.
        """
        log.info("Starting worker %s", self.__class__.__name__)
        if self._thread is not None:
            raise Exception("Called start on worker that is already running.")

        self.running = True
        self._thread = Thread(target=self._run)
        self._thread.start()

    def stop(self) -> None:
        """
        Set running to False and wait for the thread to exit until stop_timeout reached.
        Will not timeout waiting for thread to exit if stop_timeout is None.
        Throws if the worker is already stopped.
        """
        log.info("Stopping worker %s", self.__class__.__name__)
        if self._thread is None:
            raise Exception("Called stop on worker that is already stopped.")

        self.running = False
        self._thread.join(timeout=self.stop_timeout_seconds)

        if self._thread.is_alive():
            raise Exception("Worker is still running after stop timeout reached.")

        self._thread = None

    def __enter__(self) -> Self:
        self.start()
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.stop()
