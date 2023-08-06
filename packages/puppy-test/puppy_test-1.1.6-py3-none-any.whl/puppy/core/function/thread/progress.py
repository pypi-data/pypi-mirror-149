# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:is used to display testing progress
"""
import time
from threading import Thread
from ..cfg.config import config


class ProgressThread(Thread):
    __new = True
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        if ProgressThread.__new:
            super().__init__()
            self.__resource_for_db = dict()
            self.__case = "None"
            ProgressThread.__new = False

    def run(self) -> None:
        # 前往配置文件读取当前测试的案例
        while True:
            # 判断测试线程是否结束运行
            if not config.get_config("testing",bool):
                break
            if config.get_config("action_case") != self.__case:
                self.__case = config.get_config("action_case")
                # print("正在执行：{}".format(self.__case))
            time.sleep(config.get_config("progress_thread_sleep_time",int))
