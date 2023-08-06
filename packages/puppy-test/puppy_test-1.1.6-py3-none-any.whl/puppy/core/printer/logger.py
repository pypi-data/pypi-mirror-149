import logging
import sys


class Logger(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_Logger__logger"):
            cls.__logger = logging.getLogger()
            formatter = logging.Formatter('%(asctime)s:%(message)s')  # 日志的格式
            # console log 控制台输出控制
            ch = logging.StreamHandler(sys.stdout)
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            cls.__logger.addHandler(ch)
        return super().__new__(cls)

    @property
    def logger(self):
        return self.__logger


if __name__ == '__main__':
    Logger().logger.info("dddd")
