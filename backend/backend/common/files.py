import os
from typing import Union
from shutil import copytree, rmtree
from urllib3 import HTTPResponse
import pathlib


def mkdir(path: str):
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def path_exists(path: Union[pathlib.Path, str]) -> bool:
    return pathlib.Path(str(path)).exists()


def save_from_str(content: str, filepath: str):
    with open(filepath, mode="wb") as f:
        f.write(content.encode())


def save_from_response(resp: HTTPResponse, filepath: str):
    with open(filepath, mode='wb') as f:
        f.write(resp.read())


def join(root, path) -> str:
    return os.path.join(root, path)


def copy_dir(src: str, dest: str):
    copytree(src, dest)


def remove_dir(dir: str):
    rmtree(dir)
