from puppy.core import config
from datetime import datetime

from ..function.track.xml_track import xmlTrack
from ..function.beautify.fold import Fold

class DebugPrinter(object):
    __format = config.get_config("debug_format")
    #     year month day hour minute second microsecond  filename filepath line tag msg timestamp
    # 格式化输出长度
    __format_str_length = config.get_config("format_str_length", int)

    @classmethod
    def __get_format_debug_log(cls, msg):
        """
        得到适合打印的文本
        :param msg:原始日志
        :return:
        """
        text = str(msg)
        if text is None:
            return "[None]"
        text=Fold.fold_text(text)
        if len(text) >= cls.__format_str_length != -1:
            text = "{}......".format(text[:cls.__format_str_length])
        _now = datetime.now()

        year = str(_now.year).zfill(4)
        month = str(_now.month).zfill(2)
        day = str(_now.day).zfill(2)
        hour = str(_now.hour).zfill(2)
        minute = str(_now.minute).zfill(2)
        second = str(_now.second).zfill(2)
        microsecond = str(_now.microsecond)
        timestamp = str(_now.timestamp())
        filename = xmlTrack.current_file_name()
        filepath = xmlTrack.current_file_path()
        line = xmlTrack.current_row()
        tag = xmlTrack.current_tag()
        msg = text
        log = cls.__format.format(year=year, month=month, day=day, hour=hour, minute=minute, second=second,
                                  microsecond=microsecond, filename=filename, filepath=filepath, line=line, tag=tag,
                                  msg=msg, timestamp=timestamp)
        # 把换行符转为一个空格
        return log

    @classmethod
    def print_log(cls, msg):
        """
        打印日志
        :param msg:
        :return:
        """
        if not config.get_config("debug", bool):
            return
        log = cls.__get_format_debug_log(msg)
        print(log)
