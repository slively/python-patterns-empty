import os
from unittest import skip


def identity(obj):
    return obj


def runIfFileSystem():
    """
    Used to only run file system tests when the file system is available.
    This makes more sense if the 'file system' is something like a 'serial port'.
    """
    if os.environ.get("RUN_FS_TESTS", None) == "true":
        return identity
    return skip("Skipping tests that require the file system.")
