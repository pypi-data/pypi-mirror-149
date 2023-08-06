# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: is used to process regular expressions
"""
import re

from ..utils.utils import Utils
from ...exception.my_exception import MyException


class Regex(object):
    __extract_regex_re = re.compile(r"\$regex\[?([0-9]*)]?:.*")
    __replace_re = re.compile(r"\$regex\[?([0-9]*)]?:")

    def __init__(self, regex, count):
        self.__regex = re.compile(regex)
        self.__count = count

    @classmethod
    def start_with_regex(cls, st: str):
        """
        判断st是否以$regex开头
        :param st:
        :return:
        """
        if cls.__extract_regex_re.match(st) and cls.__replace_re.sub("", st) != "":
            return True
        return False

    @classmethod
    def get_real_regex(cls, st: str):
        """
        从类似“$regex[2]:aa”的st中提取regex和要取到的第几个值
        :param st:
        :return:
        """
        if not Regex.start_with_regex(st):
            return None, 0
        st_re = cls.__extract_regex_re.findall(st)
        if type(st_re) == list and len(st_re) > 0:
            count = st_re[0].strip()
            if count == "":
                count = 0
            if type(count) == str and not count.isnumeric():
                raise MyException("正则表达式格式不正确!")
            count = int(count)
            regex = cls.__replace_re.sub("", st)
            return regex, count
        else:
            return None, 0

    def get_value(self, string: str):
        """
        从string里取正则表达式获取的值，如果没有取到，则返回错误标志
        :param string:
        :return:
        """
        r = self.__regex.findall(str(string))
        if len(r) == 0:
            return Utils.ERROR
        if self.__count + 1 > len(r):
            return Utils.ERROR
        try:
            return r[self.__count]
        except Exception:
            return Utils.ERROR

    def replace_value(self, string, value):
        """
        将字符串string正则表达式指定的值设置为指定的value，并返回替换后的字符串
        :param string:
        :param value:
        :return:
        """
        string = str(string)
        r = self.__regex.finditer(str(string))
        count = 0
        for match in r:
            if count == self.__count:
                # 如果是替换此列，将次字符串拆分成两半
                index, length = match.regs[-1]
                old = string[index:length]
                front = string[:index]
                back = string[index:]
                replace = back.replace(old, value, 1)
                return "{}{}".format(front, replace)
            count += 1

    def remove_value(self, string):
        """
        从字符串移除正则表达式匹配的值，并返回移除后的字符串
        :param string:
        :return:
        """
        string = str(string)
        r = self.__regex.finditer(str(string))
        count = 0
        for match in r:
            if count == self.__count:
                # 如果是替换此列，将次字符串拆分成两半
                index, length = match.regs[-1]
                old = string[index:length]
                front = string[:index]
                back = string[index:]
                replace = back.replace(old, "", 1)
                return "{}{}".format(front, replace)
            count += 1
