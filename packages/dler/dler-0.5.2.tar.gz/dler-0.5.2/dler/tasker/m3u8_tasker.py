#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy <wxnacy@gmail.com>
# Description: m3u8 tasker

from multitasker import MultiTasker, SubTaskModel

import os
import m3u8
from typing import List
from pydantic import BaseModel

from dler.downloaders import download_url
from .base import BaseConfig, BaseTasker
from .models import DownloadTaskModel
from . import tasktools


class M3u8Tasker(MultiTasker, BaseTasker):
    download_dir: str = ""

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
            sub_tasks.append(self.build_main_sub_task())
            for ts_url in self.generate_ts_paths():
                _path = os.path.join(self.download_dir,
                    os.path.basename(ts_url))
                detail = DownloadTaskModel(url = ts_url, path = _path).dict()
                st = SubTaskModel(detail = detail, task_type = 'download')
                sub_tasks.append(st)
            return sub_tasks

        return []

    def build_main_sub_task(self) -> SubTaskModel:
        _path = os.path.join(self.download_dir,
            os.path.basename(self.url))
        detail = DownloadTaskModel(url = self.url, path = _path).dict()
        return SubTaskModel(detail = detail, task_type = 'download')


    def build_download_dir(self):
        dl_dir = os.path.join(self.Config.download_dir,
            os.path.basename(self.url).split('.')[0])
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
            #  print(i, ts_url)
            yield ts_url


M3u8Tasker.trigger_sub_task('download')(tasktools.download)
