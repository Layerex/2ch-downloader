#!/usr/bin/env python3

__prog__ = "2ch-downloader"
__desc__ = "Download all images of 2ch.hk thread"
__version__ = "0.0.1"

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path

import requests


@dataclass
class File:
    name: str
    url: str
    size: int


def download_thread_media(url: str, path: Path, max_directory_name_length: int) -> None:

    BASE_URL = "https://2ch.hk"

    api_url = url.replace(".html", ".json")

    response = json.loads(requests.get(api_url).text)

    thread = response["threads"][0]

    board = response["Board"]
    thread_id = int(response["current_thread"])
    thread_name = thread["posts"][0]["subject"]

    directory_name = f'{board} {thread_id} {thread_name.replace("/", "_")}'
    if len(directory_name) > max_directory_name_length:
        directory_name = directory_name[:max_directory_name_length]

    if not path.is_dir():
        path = path.parent
    path = path / directory_name
    os.makedirs(path, exist_ok=True)
    os.chdir(path)

    files: list[File] = []
    for post in thread["posts"]:
        for file in post["files"]:
            files.append(File(file["fullname"], BASE_URL + file["path"], file["size"]))

    for file in files:
        download_file(file)


def download_file(file: File) -> None:
    try:
        st = os.stat(file.name)
        size = st.st_size // 1024
        if size == file.size:
            print(f"{file.name} already downloaded", file=sys.stderr)
            return
    except FileNotFoundError:
        pass
    with requests.get(file.url, stream=True) as r:
        print(f"Downloading {file.name}", file=sys.stderr)
        with open(file.name, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def thread_url(url: str) -> str:
    thread_url_regex = re.compile(
        r"(?:https?:\/\/)?2ch.hk\/[a-z]+\/res\/[0-9]+.html", flags=re.I
    )
    if not thread_url_regex.match(url):
        raise ValueError("Provided url is not a thread url")
    return url


def main():
    parser = argparse.ArgumentParser(prog=__prog__)
    parser.add_argument(
        "url",
        metavar="URL",
        type=thread_url,
        help="Thread url",
    )
    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        default=".",
        help="Download directory",
    )
    parser.add_argument(
        "--max-directory-name-length",
        metavar="LENGTH",
        type=int,
        default=128,
        help="Max thread directory name length, 128 by default",
    )
    args = parser.parse_args()

    download_thread_media(
        args.url, Path(args.directory), args.max_directory_name_length
    )


if __name__ == "__main__":
    main()
