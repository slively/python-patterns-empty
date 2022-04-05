import argparse
from typing import Any
from src.utils.main.logger_utils import forwarded_logging

forwarded_logging()


def parse_args() -> Any:
    parser = argparse.ArgumentParser(description="Dir synchronizer.")
    # TODO
    return parser.parse_args()


def run() -> None:
    # args = parse_args()
    # TODO
    pass


if __name__ == "__main__":
    run()
