from lxml import etree
from urllib.parse import urlparse, ParseResult, urljoin
from collections import namedtuple
from uuid import uuid4
from os.path import basename
from typing import TypedDict, Any, List, Tuple, Optional

Scrape = namedtuple('Scrape', ['elem', 'attr'])
scrapes = [
    Scrape("script", "src"),
    Scrape("link", "href"),
    Scrape("img", "src"),
]


class ScrapeData(TypedDict):
    element: Any
    url: str
    prefix_path: str
    scrape: Tuple


class Downloadable(TypedDict):
    url: str
    save_as: str


class ScrapeResult:
    content: str
    downloads: List[Downloadable]


def get_domain(url: str) -> str:
    parsed: ParseResult = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def get_full_path(link: str, url: str) -> str:
    domain = get_domain(url)

    if link.startswith("/"):
        link = urljoin(domain, link)

    return link


def get_file(link: str, use_uuid: bool = True) -> str:
    base = basename(urlparse(link).path)
    return base if not use_uuid else f"{uuid4().hex}-{base}"


def scrape_links(config: dict) -> Optional[Downloadable]:
    e = config["element"]
    s = config["scrape"]
    link = e.get(s.attr)

    if not link or link.startswith("data:"):
        return None

    link = get_full_path(link, config["url"])
    filename = get_file(link)

    new_path = filename

    if config["prefix_path"]:
        new_path = f"{config['prefix_path']}/{filename}"

    new_link = urljoin("/", new_path)

    e.set(s.attr, new_link)

    return {"url": link, "save_as": filename}


def scrape_webpage(
    html: str,
    webpage_url: str,
    prefix_path=""
) -> dict:
    tree = etree.HTML(html)
    downloads: List[Downloadable] = []
    for s in scrapes:
        elems = tree.xpath(f'//{s.elem}')
        for e in elems:
            download: Optional[Downloadable] = scrape_links(
                {
                    "element": e,
                    "scrape": s,
                    "url": webpage_url,
                    "prefix_path": prefix_path
                }
            )
            if download:
                downloads.append(download)

    content = etree.tostring(
        tree,
        pretty_print=True,
        method="html",
        encoding='unicode'
    )
    return dict(downloads=downloads, content=content)
