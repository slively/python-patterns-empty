import os
import socket
import time
import logging
from typing import Any, Optional
from statsd import StatsClient, defaults  # type:ignore

log = logging.getLogger(__name__)
_delay_seconds_between_connection_retries = 10


class RetryingStatsClient(StatsClient):
    """
    A client for statsd that uses udp and is reslient to not finding the host on boot.
    If the host lookup fails on creation, it will be retried periodically, logging warnings.
    that metrics are failing to send.
    """

    _addr: Optional[Any] = None
    _sock: Optional[Any] = None
    _prefix: Optional[str] = None
    _ipv6: Optional[bool] = None
    _maxudpsize: Optional[int] = None
    _last_attempt: float = 0

    def __init__(
        self,
        host: str = "localhost",
        port: int = 8125,
        prefix: Optional[str] = None,
        maxudpsize: int = 512,
        ipv6: bool = False,
    ):
        """Create a new client."""
        self.host = host
        self.port = port
        self._prefix = prefix
        self._ipv6 = ipv6
        self._maxudpsize = maxudpsize

    def _send(self, data: str) -> None:
        # Socket not defined and within the retry attempt window, so retry connecting.
        if (
            self._sock is None
            and time.time() - self._last_attempt
            > _delay_seconds_between_connection_retries
        ):
            try:
                fam = socket.AF_INET6 if ipv6 else socket.AF_INET
                family, _, _, _, addr = socket.getaddrinfo(
                    self.host, self.port, fam, socket.SOCK_DGRAM
                )[0]
                self._addr = addr
                self._sock = socket.socket(family, socket.SOCK_DGRAM)
                self._prefix = prefix
                log.info(
                    "Successfully connected to StatsD host %s:%s",
                    self.host,
                    str(self.port),
                )
            except Exception as e:
                log.exception(
                    "Failed to connect to StatsD host %s:%s : %s",
                    self.host,
                    self.port,
                    e,
                )

        # No connection, log a warning and drop the metric.
        if self._sock is None:
            log.warning("Dropping statsd metric because cannot reach host: %s", data)
            return

        # Copied from original implementation.
        try:
            self._sock.sendto(data.encode("ascii"), self._addr)
        except (socket.error, RuntimeError):
            # No time for love, Dr. Jones!
            pass


"""
Copied from statsd.defaults.env
Uses the default environment configured statsd client.
Details here: https://statsd.readthedocs.io/en/v3.3/configure.html#from-the-environment
The available environment variables to configure this client are:
    STATSD_HOST=localhost
    STATSD_PORT=8125
    STATSD_PREFIX=None
    STATSD_MAXUDPSIZE=512
    STATSD_IPV6=0
"""
host = os.getenv("STATSD_HOST", defaults.HOST)
port = int(os.getenv("STATSD_PORT", defaults.PORT))
prefix = os.getenv("STATSD_PREFIX", defaults.PREFIX)
maxudpsize = int(os.getenv("STATSD_MAXUDPSIZE", defaults.MAXUDPSIZE))
ipv6 = bool(int(os.getenv("STATSD_IPV6", defaults.IPV6)))
statsd: RetryingStatsClient = RetryingStatsClient(
    host=host, port=port, prefix=prefix, maxudpsize=maxudpsize, ipv6=ipv6
)
