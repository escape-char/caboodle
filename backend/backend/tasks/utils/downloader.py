from typing import List, Final
from urllib3 import PoolManager
from urllib3.exceptions import HTTPError
from backend.common.files import save_from_response, join
from .scraper import Downloadable


def download_file(http: PoolManager, d: Downloadable, save_path: str):
    try:
        with http.request("GET", d["url"]) as resp:
            path: Final[str] = join(save_path, d["save_as"])
            save_from_response(resp, path)
    except HTTPError as e:
        print("e: ", e)
        pass


def download_dispatcher(
    http: PoolManager, download_urls: List[Downloadable], save_path: str
):
    pass
