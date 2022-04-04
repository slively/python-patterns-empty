import hashlib
import os
import shutil


def get_all_files_in_dir(target_dir: str) -> list:
    filenames = []
    for root, subdirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            filenames.append(os.path.join(root, file))
    return filenames


def get_md5_of_file(filepath: str) -> str:
    with open(filepath, "rb") as file_to_check:
        # read contents of the file
        data = file_to_check.read()
        # pipe contents of the file through
        md5_returned = hashlib.md5(data).hexdigest()
    return md5_returned


def clean_and_remake_dir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path, ignore_errors=True)
    os.mkdir(path)
