
from abc import abstractmethod
from queue import Queue
from typing import Generic, TypeVar


T = TypeVar("T")


class SendEventQueue(Generic[T]):
    @abstractmethod
    def send(self, item: T) -> None:
        raise NotImplementedError


class ReceiveEventQueue(Generic[T]):
    @abstractmethod
    def receive(self) -> T:
        raise NotImplementedError


class EventQueue(SendEventQueue[T], ReceiveEventQueue[T]):
    def __init__(self, queue: Queue, get_timeout_seconds: int) -> None:
        self.queue = queue
        self.get_timeout_seconds = get_timeout_seconds

    def send(self, item: T) -> None:
        self.queue.put(item)

    def receive(self) -> T:
        return self.queue.get(timeout=self.get_timeout_seconds)
