from time import sleep, time
from typing import Callable
from xmlrpc.client import Boolean


def sleep_until(
    predicate: Callable[[], Boolean], timeout: int = 10, period: float = 0.1
) -> None:
    """
    Sleep the current thread until predicate returns true.
    Will check the predicate every period seconds until timeout seconds is reached after which an exception is thrown.
    """
    mustend = time() + timeout
    while time() < mustend:
        if predicate():
            return
        sleep(period)
    raise Exception("Timeout waiting for condition")


def sleep_ms(time_in_ms: float) -> None:
    """
    Just like time.sleep(seconds), but milliseconds instead of seconds.
    """
    time_in_s = time_in_ms / 1000
    sleep(time_in_s)
