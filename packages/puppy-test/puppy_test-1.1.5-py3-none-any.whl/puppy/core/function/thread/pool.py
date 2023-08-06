# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:is used to save all kinds of resources
"""
import time
from threading import Thread, Lock

from ..cfg.config import config
from ..database.db import DB, DBRes


class ResourcePool(Thread):
    __new = True
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        # 创建一个锁
        if ResourcePool.__new:
            super().__init__()
            self.__resource_for_db = dict()
            self.__lock = Lock()
            ResourcePool.__new = False

    def exec_sql(self, db_info, sql) -> DBRes:
        """
        执行sql语句
        """
        db_and_use_time = self.__resource_for_db.get(db_info)
        db = None
        if db_and_use_time:
            db = db_and_use_time[1]
        if db is None:
            db = DB(db_info)
        try:
            self.__lock.acquire()
            res = db.execute(sql)
            self.__resource_for_db[db_info] = [time.time(), db]
        except Exception as e:
            raise e
        else:
            return res
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def run(self) -> None:
        while True:
            # 判断测试线程是否结束运行
            if not config.get_config("testing",bool):
                for use_date, db in self.__resource_for_db.values():
                    try:
                        self.__lock.acquire()
                        db.close()
                    except Exception as e:
                        raise e
                    finally:
                        if self.__lock.locked():
                            self.__lock.release()
                break
            # 遍历db资源，根据时间对其进行处理
            for use_date, db in self.__resource_for_db.values():
                try:
                    self.__lock.acquire()
                    now = time.time()
                    if now - use_date > config.get_config("db_keep_connection_time",int):
                        # 已经超过释放时间
                        db.close()
                except Exception as e:
                    raise e
                finally:
                    if self.__lock.locked():
                        self.__lock.release()
            # 线程睡眠指定时间
            time.sleep(config.get_config("resource_thread_sleep_time"))

    def close(self):
        """
        关闭链接
        """
        for use_date, db in self.__resource_for_db.values():
            db.close()
