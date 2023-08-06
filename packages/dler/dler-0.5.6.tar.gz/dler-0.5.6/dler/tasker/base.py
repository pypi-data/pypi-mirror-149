from typing import Dict, Any
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

    class Config(BaseConfig):
        pass

    def __init__(self,
            url: str, filename: str = None, config: Dict[str, Any] = None
    ) -> None:
        self.url = url
        self.urlparse = urlparse(url)
        self.filename = filename
        filenames = filename.split('.')
        self.filetype = filenames[1] if len(filenames) > 1 else None

        for key, value in config.items():
            setattr(self.Config, key, value)

    def after_run(self):
        pass

    def before_run(self):
        pass

