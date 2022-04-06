from abc import abstractmethod
from queue import Empty, Queue
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class SendEventQueue(Generic[T]):
    @abstractmethod
    def send(self, item: T) -> None:
        raise NotImplementedError


class ReceiveEventQueue(Generic[T]):
    @abstractmethod
    def receive(self) -> Optional[T]:
        raise NotImplementedError


class EventQueue(SendEventQueue[T], ReceiveEventQueue[T]):
    def __init__(
        self, queue: Queue = Queue(), get_timeout_seconds: float = 0.1
    ) -> None:
        self.queue = queue
        self.get_timeout_seconds = get_timeout_seconds

    def send(self, item: T) -> None:
        self.queue.put(item)

    def receive(self) -> Optional[T]:
        try:
            return self.queue.get(timeout=self.get_timeout_seconds)
        except Empty:
            return None
