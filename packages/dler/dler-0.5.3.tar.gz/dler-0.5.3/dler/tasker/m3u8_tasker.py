#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy <wxnacy@gmail.com>
# Description: m3u8 tasker

from multitasker import MultiTasker, SubTaskModel

import os
import m3u8
from urllib.parse import urlparse
from m3u8.model import Segment
from typing import List
from wpy.functools import run_shell

from .base import BaseConfig, BaseTasker
from .models import DownloadTaskModel
from . import tasktools


class M3u8Tasker(MultiTasker, BaseTasker):
    download_dir: str = ""
    filepath: str = ""

    class Config(BaseConfig):
        task_type: str = 'm3u8'

    def build_task(self) -> dict:
        detail = {}
        if self.url:
            detail['url'] = self.url
            self.download_dir = self.build_download_dir()

        return {}

    def build_sub_tasks(self) -> List[SubTaskModel]:

        sub_tasks = []
        if self.url:
            sub_tasks.append(self.build_dl_m3u8_sub_task())
            for ts_url in self.generate_ts_paths():
                _path = os.path.join(self.download_dir,
                    os.path.basename(ts_url))
                detail = DownloadTaskModel(url = ts_url, path = _path).dict()
                st = SubTaskModel(detail = detail, task_type = 'download')
                sub_tasks.append(st)
            return sub_tasks

        return []

    def build_dl_m3u8_sub_task(self) -> SubTaskModel:
        filename = f'{self.filename}.m3u8' or os.path.basename(self.urlparse.path)
        _path = os.path.join(self.download_dir, filename)
        self.filepath = _path
        detail = DownloadTaskModel(url = self.url, path = _path).dict()
        return SubTaskModel(detail = detail, task_type = 'download_m3u8')


    def build_download_dir(self):
        filename = self.filename or os.path.basename(self.url).split('.')[0]
        dl_dir = os.path.join(self.Config.download_dir, filename)
        if not os.path.exists(dl_dir):
            os.mkdir(dl_dir)
        return dl_dir

    def generate_ts_paths(self):
        m3 = m3u8.load(self.url)
        for i, name in enumerate(m3.files):
            if not name:
                continue
            ts_url = name
            if not ts_url.startswith('http'):
                ts_url = os.path.join(m3.base_uri, ts_url)
            yield ts_url

    def transcoding(self, trans_type: str):
        trans_path = os.path.join(self.Config.download_dir,
                os.path.basename(self.filepath).replace('m3u8', trans_type))
        cmd = f'ffmpeg -allowed_extensions ALL -i {self.filepath} -bsf:a aac_adtstoasc -vcodec copy -c copy -crf 50 {trans_path}'
        run_shell(cmd)

M3u8Tasker.trigger_sub_task('download')(tasktools.download)

@M3u8Tasker.trigger_sub_task('download_m3u8')
def download_m3u8(sub_task: SubTaskModel) -> bool:
    flag = tasktools.download(sub_task)
    if flag:
        # 修改 m3u8 文件
        task = DownloadTaskModel(**sub_task.detail)
        m3 = m3u8.load(task.path)
        seg: Segment
        for seg in m3.segments:
            seg.uri = os.path.basename(urlparse(seg.uri).path)
        m3.dump(task.path)

    return flag

