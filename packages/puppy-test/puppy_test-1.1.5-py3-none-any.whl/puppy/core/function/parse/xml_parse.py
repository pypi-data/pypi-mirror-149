# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: parse of xml data
"""
import re
from ..parse.key.point import PointKey
from ..utils.utils import Utils
from ...exception.my_exception import MyException


class XmlParse(object):
    __check_re = re.compile(r"<\w>.*</\w>")
    __special_str = "~||@||~"

    def __init__(self, xml: str):
        """
        xml字符串提取器
        :param xml:
        """
        if xml:
            xml = xml.strip()
        else:
            xml = ""
        xml = xml.replace("\n", XmlParse.__special_str,-1)
        self.__xml = xml

    def get_value(self, key: str):
        """
        从xml获取的值，如果没有取到，则返回错误标志
        :return:
        """
        point_key = PointKey(key)
        try:
            res=self.__get_detail(point_key, self.__xml)
            return res.replace(XmlParse.__special_str,"\n",-1)
        except Exception:
            return Utils.ERROR

    def replace_value(self, key, value):
        """
        将字xml指定的值设置为指定的value，并返回替换后的字符串
        :param value:
        :param key:
        :return:
        """
        point_key = PointKey(key)
        try:
            res=self.__replace_detail(point_key, self.__xml, value)
            return res.replace(XmlParse.__special_str, "\n", -1)
        except Exception:
            return None

    def remove_value(self, key: str):
        """
        从xml匹配的值，并返回移除后的字符串
        :return:
        """
        point_key = PointKey(key)
        try:
            res= self.__remove_detail(point_key, self.__xml)
            return res.replace(XmlParse.__special_str, "\n", -1)
        except Exception:
            return None

    def insert_value(self, key: str, value):
        """
        插入
        """
        point_key = PointKey(key)
        try:
            res= self.__insert_detail(point_key, value, self.__xml, True)
            return res.replace(XmlParse.__special_str, "\n", -1)
        except Exception:
            return None

    def __replace_detail(self, point_key, xml, value):
        """
        替换细节
        :param xml:
        :param value:
        :return:
        """
        if point_key.size() == 0:
            return value
        if point_key.is_index_next_key():
            raise MyException("提取表达式格式不正确！")
        key = point_key.next()
        number = 0
        if point_key.is_index_next_key():
            number = point_key.next()
        # 带有数字的提取的key
        if XmlParse.is_contained(xml, key) and int(number) > 1:
            raise MyException("提取表达式格式不正确!")
        if XmlParse.is_contained(xml, key):
            # 如果式包含的
            res = re.finditer("<{}>(.*)</{}>".format(key, key), xml)
            for r in res:
                left_index, right_index = r.span(1)
                left_str = xml[:left_index]
                right_str = xml[right_index:]
                return "{}{}{}".format(left_str, self.__replace_detail(point_key, xml[left_index:right_index], value),
                                       right_str)
        else:
            # 如果式并列的
            count = 0
            res = re.finditer("<{}>(.*?)</{}>".format(key, key), xml)
            for r in res:
                if int(number) == count:
                    left_index, right_index = r.span(1)
                    left_str = xml[:left_index]
                    right_str = xml[right_index:]
                    return "{}{}{}".format(left_str,
                                           self.__replace_detail(point_key, xml[left_index:right_index], value),
                                           right_str)
                if count > int(number):
                    raise MyException("提取表达式格式不正确!")
                count += 1
            raise MyException("提取表达式格式不正确!")

    def __remove_detail(self, point_key, xml):
        """
        移除细节
        :return:
        """
        if point_key.is_index_next_key():
            raise MyException("提取表达式格式不正确！")
        key = point_key.next()
        number = 0
        if point_key.is_index_next_key():
            number = point_key.next()
        if XmlParse.is_contained(xml, key) and int(number) > 1:
            raise MyException("提取表达式格式不正确!")
        if XmlParse.is_contained(xml, key):
            # 如果式包含的
            if point_key.size() == 0:
                # 如果式并列的
                count = 0
                res = re.finditer("(<{}>.*?</{}>)".format(key, key), xml)
                for r in res:
                    if int(number) == count:
                        left_index, right_index = r.span(1)
                        left_str = xml[:left_index]
                        right_str = xml[right_index:]
                        return "{}{}".format(left_str, right_str)
                    if count > int(number):
                        raise MyException("提取表达式格式不正确!")
                    count += 1
                raise MyException("提取表达式格式不正确!")
            else:
                res = re.finditer("<{}>(.*)</{}>".format(key, key), xml)
                for r in res:
                    left_index, right_index = r.span(1)
                    left_str = xml[:left_index]
                    right_str = xml[right_index:]
                    return "{}{}{}".format(left_str, self.__remove_detail(point_key, xml[left_index:right_index]),
                                           right_str)
        else:
            if point_key.size() == 0:
                # 如果式并列的
                count = 0
                res = re.finditer("(<{}>.*?</{}>)".format(key, key), xml)
                for r in res:
                    if int(number) == count:
                        left_index, right_index = r.span(1)
                        left_str = xml[:left_index]
                        right_str = xml[right_index:]
                        return "{}{}".format(left_str, right_str)
                    if count > int(number):
                        raise MyException("提取表达式格式不正确!")
                    count += 1
                raise MyException("提取表达式格式不正确!")
            else:
                # 如果式并列的
                count = 0
                res = re.finditer("<{}>(.*?)</{}>".format(key, key), xml)
                for r in res:
                    if int(number) == count:
                        left_index, right_index = r.span(1)
                        left_str = xml[:left_index]
                        right_str = xml[right_index:]
                        return "{}{}{}".format(left_str, self.__remove_detail(point_key, xml[left_index:right_index]),
                                               right_str)
                    if count > int(number):
                        raise MyException("提取表达式格式不正确!")
                    count += 1
                raise MyException("提取表达式格式不正确!")

    def __get_detail(self, point_key, xml):
        """
        查找细节
        :return:
        """
        if point_key.size() == 0:
            return xml
        if point_key.is_index_next_key():
            raise MyException("提取表达式格式不正确！")
        key = point_key.next()
        number = 0
        if point_key.is_index_next_key():
            number = point_key.next()
        # 带有数字的提取的key
        if XmlParse.is_contained(xml, key) and int(number) > 1:
            raise MyException("提取表达式格式不正确!")
        if XmlParse.is_contained(xml, key):
            # 如果式包含的
            res = re.finditer("<{}>(.*)</{}>".format(key, key), xml)
            for r in res:
                left_index, right_index = r.span(1)
                return self.__get_detail(point_key, xml[left_index:right_index])
        else:
            # 如果式并列的
            count = 0
            res = re.finditer("<{}>(.*?)</{}>".format(key, key), xml)
            for r in res:
                if int(number) == count:
                    left_index, right_index = r.span(1)
                    return self.__get_detail(point_key, xml[left_index:right_index])
                if count > int(number):
                    raise MyException("提取表达式格式不正确!")
                count += 1
            raise MyException("提取表达式格式不正确!")

    def __insert_detail(self, point_key: PointKey, value, xml, first=False):
        """
        插入细节
        """
        if point_key.size() <= 0:
            return value
        if point_key.size() > 0:
            if point_key.is_index_next_key():
                raise MyException("提取表达式格式不正确！")
            tag = point_key.next()
            index = 0
            if point_key.is_index_next_key():
                index = point_key.next()
            # 找到当前节点对应的值
            count = 0
            res = re.finditer("<{}>(.*?)</{}>".format(tag, tag), xml)
            for r in res:
                if int(index) == count:
                    # 查找到了，继续迭代
                    left_index, right_index = r.span(1)
                    left_str = xml[:left_index]
                    right_str = xml[right_index:]
                    return "{}{}{}".format(left_str,
                                           self.__insert_detail(point_key, value, xml[left_index:right_index]),
                                           right_str)
                count += 1
            else:
                # 未查找到，进行创建
                if first:
                    return "<{}>{}</{}>".format(tag, self.__create_tag(point_key, value), tag)
                else:
                    return "{}<{}>{}</{}>".format(xml, tag, self.__create_tag(point_key, value), tag)

    def __create_tag(self, point_key: PointKey, value):
        """
        创建标签
        """
        if point_key.size() == 0:
            return value
        if point_key.size() > 0:
            if point_key.is_index_next_key():
                raise MyException("提取表达式格式不正确！")
            tag = point_key.next()
            if point_key.is_index_next_key():
                point_key.next()
            return "<{}>{}</{}>".format(tag, self.__create_tag(point_key, value), tag)

    @classmethod
    def is_contained(cls, xml: str, tag: str):
        """
        是否包含关系
        :param xml:
        :param tag:
        :return:
        """
        regex = "<{}>(.*)</{}>".format(tag, tag)
        extract_re_by_greed = re.compile(regex)
        extracted_str = extract_re_by_greed.findall(xml)[0]
        if cls.__check_re.match(extracted_str.strip()):
            return True
        else:
            return False
