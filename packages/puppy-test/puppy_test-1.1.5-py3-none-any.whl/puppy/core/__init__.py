# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    describe:This is a test frame about api, before using it, please copy the file dir as your project dir.
"""
from .function.cfg.config import config
from .function import ProgressThread
from .function.thread.pool import ResourcePool

config = config
ProgressThread = ProgressThread
ResourcePool = ResourcePool



