# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:  Base Exception
"""
from ..function.track.xml_track import xmlTrack


class MyException(Exception):
    def __init__(self, e, file_path=None, row_number=None):
        if file_path is None or row_number is None:
            self.__file_path, self.__row_number = xmlTrack.current_path_row()
        else:
            self.__file_path = file_path
            self.__row_number = row_number
        if type(e) is not str:
            self.__name = e.__class__.__name__
            self.__msg = e.__str__()
        else:
            self.__msg = e

    def error(self):
        if hasattr(self, "_MyException__name"):
            return '\n  File "{}", line {}\n{}:\n  {}'.format(self.__file_path, self.__row_number, self.__name,
                                                              self.__msg)
        else:
            return '\n  File "{}", line {}\nMyException:\n  {}'.format(self.__file_path, self.__row_number, self.__msg)

    def __str__(self):
        return self.error()
