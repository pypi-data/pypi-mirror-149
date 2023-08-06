import importlib.metadata

__version__ = importlib.metadata.version("simple_downloader")

from pathlib import Path
from urllib.parse import urlparse

import requests
from pydantic import AnyHttpUrl, DirectoryPath, validate_arguments

# from tqdm.auto import tqdm
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

progress = Progress(
    TextColumn("[bold]{task.fields[file_name]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.1f}%",
    "|",
    DownloadColumn(),
    "|",
    TransferSpeedColumn(),
    "|",
    TimeRemainingColumn(),
    auto_refresh=True,
    refresh_per_second=10,
)


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
        with open(target_file, mode="wb") as output:
            with progress:
                t_id = progress.add_task(
                    "Downloading...", total=total_length, file_name=file_name
                )
                for chunk in r.iter_content(chunk_size=1024):
                    output.write(chunk)
                    progress.update(t_id, advance=len(chunk))
    return target_file
