import argparse
from logging import getLogger
from src.file_syncer.main.simple_main import Worker
from src.utils.main.logger_utils import basic_logging

basic_logging()
log = getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Example embedded project daemon.")
    parser.add_argument("--dir", help="Directory to watch.", required=True)
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=False
    )
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser(name="list", description="List files in dir.")
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    worker = Worker(args.dir, args.sync_dir)

    if args.command == "list":
        print(worker.list_files())


if __name__ == "__main__":
    run()
