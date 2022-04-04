import argparse
from glob import glob
from logging import getLogger
import os
from posixpath import basename
from threading import Thread
from time import sleep
from typing import Dict, List, Optional
from pydantic import BaseModel
from src.utils.main.logger_utils import forwarded_logging
from src.utils.main.statsd_utils import statsd

forwarded_logging()
log = getLogger(__name__)


class FileModel(BaseModel):
    name: str
    path: str
    is_dir: bool
    contents: str


class Worker:
    """
    This worker should sync files from one directory to another and log messages and metrics.
    Any file that is added/deleted/modified in one directory should be reflected in the other
    directory within some period of time.
    """

    _current_files: List[FileModel] = []
    new_file_count = 0
    deleted_file_count = 0
    changed_file_count = 0

    def __init__(self, dir: str, sync_dir: Optional[str]):
        self.dir = dir
        self.sync_dir = sync_dir

    def start(self) -> None:
        log.info("Starting worker %s", self.__class__.__name__)
        self.running = True
        self._thread = Thread(target=self._run)
        self._thread.start()

    def stop(self) -> None:
        log.info("Stopping worker.")
        self.running = False
        if self._thread is not None:
            self._thread.join()

    def list_files(self) -> List[FileModel]:
        files = []
        # get all the file paths
        paths = glob(self.dir + "/**", recursive=True)

        # for each path turn it into a file model and add it to the files list
        for p in paths:
            name = basename(p)
            path_relative_to_root = os.path.relpath(p, self.dir)

            # skip the root dir
            if path_relative_to_root == ".":
                continue
            elif os.path.isdir(p):
                files.append(
                    FileModel(
                        path=path_relative_to_root,
                        name=name,
                        contents="",
                        is_dir=True,
                    )
                )
            else:
                with open(p, mode="r") as f:
                    files.append(
                        FileModel(
                            path=path_relative_to_root,
                            name=name,
                            is_dir=False,
                            contents=f.read(),
                        )
                    )

        return files

    def _current_files_by_path(self) -> Dict[str, FileModel]:
        return {file.path: file for file in self._current_files}

    def _run(self) -> None:
        """
        Polls the DirReaderApi in a loop while tracking and logging any changes.
        """
        while self.running:
            change_detected = False
            files = self.list_files()

            previous_files_by_path = self._current_files_by_path()
            self._current_files = files
            current_files_by_path = self._current_files_by_path()

            previous_file_paths = previous_files_by_path.keys()
            current_file_paths = current_files_by_path.keys()

            deleted_file_paths = previous_file_paths - current_file_paths
            if len(deleted_file_paths) > 0:
                change_detected = True
                self.deleted_file_count += 1
                log.info("Files deleted: %s", ", ".join(deleted_file_paths))

                if self.sync_dir is not None:
                    for file_path in deleted_file_paths:
                        full_path = os.path.join(self.sync_dir, file_path)
                        log.info("Synchronizing delete %s", file_path)
                        file = previous_files_by_path[file_path]
                        if file.is_dir:
                            os.rmdir(full_path)
                        else:
                            os.remove(full_path)

            new_file_paths = list(current_file_paths - previous_file_paths)
            if len(new_file_paths) > 0:
                change_detected = True
                self.new_file_count += 1
                log.info("Files created: %s", ", ".join(new_file_paths))

            existing_files = current_file_paths - new_file_paths
            changed_file_paths = []
            for file_path in existing_files:
                previous_content = previous_files_by_path[file_path].contents
                current_content = current_files_by_path[file_path].contents
                if previous_content != current_content:
                    changed_file_paths.append(file_path)

            if self.sync_dir is not None:
                for file_path in new_file_paths + changed_file_paths:
                    full_path = os.path.join(self.sync_dir, file_path)
                    log.info("Synchronizing change %s", file_path)
                    file = current_files_by_path[file_path]
                    if file.is_dir:
                        os.mkdir(full_path)
                    else:
                        with open(full_path, "w+") as f:
                            f.write(file.contents)

            if len(changed_file_paths) > 0:
                change_detected = True
                self.changed_file_count += 1
                log.info("Files changed: %s", ", ".join(changed_file_paths))

            if not change_detected:
                log.info("No changes detected.")

            statsd.gauge("new_file_count", self.new_file_count)
            statsd.gauge("changed_file_count", self.changed_file_count)
            statsd.gauge("deleted_file_count", self.deleted_file_count)

            sleep(2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="File syncer daemon.")
    parser.add_argument("--dir", help="Directory to watch.", required=True)
    parser.add_argument(
        "--sync_dir", help="Local directory to sync changes to.", required=False
    )
    return parser.parse_args()


def run() -> None:
    args = parse_args()
    worker = Worker(args.dir, args.sync_dir)
    worker.start()


if __name__ == "__main__":
    run()
