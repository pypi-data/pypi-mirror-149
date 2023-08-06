#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import typer
import time
#  from urllib.parse import urlparse
#  from multitasker import MultiTasker
from typer import Argument, Option

from dler import conver_tasker

app = typer.Typer()

@app.command()
def start(
    url: str = Argument(..., help="URL 路径"),
    name: str = Option(None, '-n', '--name', help="下载文件保存名"),
    trans: str = Option(None, '-t', '--trans', help="转码"),
):
    """开始下载任务"""

    begin = time.time()
    tasker = conver_tasker(url, filename = name)
    tasker.build()
    tasker.run()
    tasker.after_run()

    cost = time.time() - begin
    typer.echo(f'下载完成，耗时: {cost}')


@app.command()
def run():
    print('test')

if __name__ == "__main__":
    app()
