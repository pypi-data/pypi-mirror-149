
from .models import DownloadTaskModel
from dler.downloaders import download_url


def download(sub_task) -> bool:
    """下载任务"""
    task = DownloadTaskModel(**sub_task.detail)
    return download_url(task.url, task.path, headers = task.headers)
