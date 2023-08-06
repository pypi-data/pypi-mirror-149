import importlib.metadata

__version__ = importlib.metadata.version("simple_downloader")

import shutil
from pathlib import Path
from urllib.parse import urlparse

import requests
from pydantic import AnyHttpUrl, DirectoryPath, validate_arguments
from tqdm.auto import tqdm


@validate_arguments
def download(url: AnyHttpUrl, target_dir: DirectoryPath, force: bool = False) -> Path:
    """
    Download the file from `url` to the `target_dir`, where the name is the name of the downloaded file.
    The path to the downloaded file is returned.
    """
    file_name = Path(urlparse(url).path).name
    target_file = target_dir / file_name
    if target_file.exists() and not force:
        print("Target file already exists!")
        print("Will skip download. To force download set `force=True`")
        return target_file

    with requests.get(url, stream=True) as r:
        total_length = int(r.headers.get("Content-Length"))
        with tqdm.wrapattr(
            r.raw, "read", total=total_length, desc=f"Downloading {file_name}"
        ) as raw:
            with open(target_file, "wb") as output:
                shutil.copyfileobj(raw, output)
    return target_file
