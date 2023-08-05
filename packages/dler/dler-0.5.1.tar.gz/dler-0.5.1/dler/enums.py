#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from wpy.base import BaseEnum

#  class TaskStatus(BaseEnum):
    #  WAITING = 'waiting'
    #  SUCCESS = 'success'
    #  FAILED = 'failed'
    #  PROCESS = 'process'
    #  STOP = 'stop'
    #  SLEEP = 'sleep'

class FileType(BaseEnum):
    IMAGE = 'image'
    #  video = 'video'
    M3U8 = 'm3u8'

    @classmethod
    def get_filetype_by_url(cls, url):
        suffix = url.split('.')[-1] if '.' in url else url
        if cls.is_valid(suffix):
            return suffix
        return None

