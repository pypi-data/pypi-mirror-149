#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import typer
from urllib.parse import urlparse
from multitasker import MultiTasker
from typer import Argument, Option

from dler.tasker import (
    M3u8Tasker,
    FileTasker
)

app = typer.Typer()

def conver_tasker(url: str) -> MultiTasker:
    parse = urlparse(url)
    path = parse.path
    Tasker = None
    if path.endswith('.m3u8'):
        Tasker = M3u8Tasker
    else:
        Tasker = FileTasker

    return Tasker(url)

@app.command()
def start(
    url: str = Argument(..., help="URL 路径"),
    name: str = Option(None, '-n', '--name', help="下载文件保存名"),
    trans: str = Option(None, '-t', '--trans', help="转码"),
):
    """开始下载任务"""

    tasker = conver_tasker(url)
    tasker.filename = name
    tasker.build()
    tasker.run()

    if trans:
        tasker.transcoding(trans)


@app.command()
def run():
    print('test')

if __name__ == "__main__":
    app()
