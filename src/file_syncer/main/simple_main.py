import argparse
from logging import getLogger
from src.utils.main.logger_utils import forwarded_logging

forwarded_logging()
log = getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="File syncer daemon.")
    parser.add_argument("--dir", help="Directory to watch.", required=True)
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=False
    )
    return parser.parse_args()


def run() -> None:
    # /args = parse_args()
    # worker = Worker(args.dir, args.sync_dir)
    # worker.start()
    print("todo")


if __name__ == "__main__":
    run()
