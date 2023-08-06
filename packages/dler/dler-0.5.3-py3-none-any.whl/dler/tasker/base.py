from urllib.parse import urlparse, ParseResult

from dler.constants import DOWNLOAD_DIR, ENV_DOWNLOAD_DIR

class BaseConfig:
    task_type: str
    download_dir: str = ENV_DOWNLOAD_DIR or DOWNLOAD_DIR

class BaseTasker:
    url: str
    filename: str = ""
    urlparse: ParseResult

    def __init__(self, url: str):
        self.url = url
        self.urlparse = urlparse(url)
