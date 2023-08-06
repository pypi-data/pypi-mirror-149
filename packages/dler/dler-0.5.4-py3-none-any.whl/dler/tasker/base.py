from urllib.parse import urlparse, ParseResult
from multitasker import MultiTasker

from dler.constants import DOWNLOAD_DIR, ENV_DOWNLOAD_DIR

class BaseConfig:
    task_type: str
    download_dir: str = ENV_DOWNLOAD_DIR or DOWNLOAD_DIR

class BaseTasker(MultiTasker):
    url: str
    filename: str
    filetype: str
    urlparse: ParseResult

    def __init__(self, url: str, filename: str):
        self.url = url
        self.urlparse = urlparse(url)
        self.filename = filename
        filenames = filename.split('.')
        self.filetype = filenames[1] if len(filenames) > 1 else None

    def after_run(self):
        pass

    def before_run(self):
        pass

