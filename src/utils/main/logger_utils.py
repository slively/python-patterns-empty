"""
Functions to setup standard logging configurations.
"""
import logging
import os
import platform
from logging.handlers import SocketHandler
from typing import Any
from pythonjsonlogger import jsonlogger  # type: ignore


loglevel = os.environ.get("LOGLEVEL", "INFO").upper()


def basic_logging() -> None:
    logging.basicConfig(level=loglevel)


def forwarded_logging() -> None:
    """
    To set the global log level use the LOGLEVEL environment variable: LOGLEVEL=DEBUG
    To set the local tcp port for JSON logs use JSON_LOGS_TCP_PORT: JSON_LOGS_TCP_PORT=5170
    """

    json_logs_tcp_port = int(os.environ.get("JSON_LOGS_TCP_PORT", "5170"))
    logger = logging.getLogger()
    logger.setLevel(loglevel)

    """
    Log all messages to the console with default formatter.
    """
    stdOutHandler = logging.StreamHandler()
    stdOutHandler.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logger.addHandler(stdOutHandler)

    class HostnameFilter(logging.Filter):
        """
        Filter that adds hostname property to all log messages.
        """

        hostname = platform.node()

        def filter(self, record: Any) -> bool:
            record.hostname = self.hostname
            return True

    class PlainTextTcpHandler(SocketHandler):
        """
        Normally the Python TCP logger turns messages into a 'pickle' format, we skip that here and use its formatter.
        """

        def makePickle(self, record: logging.LogRecord) -> bytes:
            if self.formatter is None:
                raise Exception("Formatter required for PlainTextTcpHandler!")

            message = self.formatter.format(record) + "\r\n"
            return message.encode()

    """
    Also log all messages as json to TCP localhost:5170 where fluent-bit collects logs.
    These logs are formatted as JSON and include the hostname.
    """
    socketHandler = PlainTextTcpHandler("localhost", json_logs_tcp_port)
    socketHandler.addFilter(HostnameFilter())
    socketHandler.setFormatter(
        jsonlogger.JsonFormatter("%(message)%(levelname)%(name)%(asctime)%(hostname)")
    )
    logger.addHandler(socketHandler)
