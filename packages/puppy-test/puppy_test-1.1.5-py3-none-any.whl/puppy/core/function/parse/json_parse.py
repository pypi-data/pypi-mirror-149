# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: is used to parse json data
"""
import json

from ...exception.my_exception import MyException
from ..utils.utils import Utils
from ..parse.key.point import PointKey


class JsonParse(object):
    """
    json解析器，提供一系列的json相关功能
    """

    def __init__(self, jsons):
        self.__json = None
        self.__json_str = None
        if type(jsons) in [dict, list]:
            self.__json = jsons
        if type(jsons) == str:
            self.__json_str = jsons
        if self.__json is None:
            self.__json = self.to_json(self.__json_str)

    @classmethod
    def is_correct_json(cls, json_str: str):
        """
        测试json字符串是正确格式的json
        :param json_str: 
        :return: 
        """
        try:
            json.loads(json_str)
        except Exception:
            return False
        return True

    @classmethod
    def is_correct_json_dict(cls, json_str: str):
        """
        测试jison字符串是正确格式的json字典吗
        :param json_str:
        :return:
        """
        try:
            json_o = json.loads(json_str)
            return type(json_o) == dict
        except Exception:
            return False

    @classmethod
    def loads(cls, json_str: str):
        """
        json字符串转字典
        :param json_str:
        :return:
        """
        ret = cls.to_json(json_str)
        if ret is None:
            raise MyException("不是正确的json字符串 {} ".format(json_str))
        return ret

    @classmethod
    def to_json(cls, json_str):
        """
        json字符串转json字典
        :param json_str:
        :return:
        """
        try:
            return json.loads(json_str)
        except Exception:
            return None

    @classmethod
    def dumps(cls, json: dict):
        """
        将字典或列表转为json字符串
        :return:
        """
        return cls.to_json_str(json)

    @classmethod
    def to_json_str(cls, json_o: dict):
        """
        将字典或列表转为json字符串
        :return:
        """
        if type(json_o) not in [dict, list]:
            raise MyException("应是dict或list，而不是{}".format(type(json_o)))
        return json.dumps(json_o)

    @classmethod
    def to_good_json_str(cls, json_dict: dict):
        """
        将字典或列表转为好看的json字符串
        :return:
        """
        if type(json_dict) not in [dict, list]:
            raise MyException("应是dict或list，而不是{}".format(type(json_dict)))
        return json.dumps(json_dict).encode("utf-8").decode(encoding="raw-unicode-escape")

    def is_contained_the_key(self, key: str):
        """
        判断是否包含这个key
        :param key:
        :return:
        """
        return self.get_value(key) is not Utils.ERROR

    def get_value(self, key: str):
        """
        key:a.a[1].b
        json:
        从json里取到key对应的值，未取到则返回错误标志
        :param key:
        :return:
        """
        json_o = self.__json
        point_key = PointKey(key)
        try:
            while point_key.has():
                k = point_key.next()
                # 判断待处理的数据是否是列表
                if type(k) != int:
                    # 不是索引
                    if type(json_o) is list:
                        json_o = json_o[0]
                json_o = json_o[k]
            return json_o
        except Exception:
            return Utils.ERROR

    def replace_value(self, key, value):
        """
        得到替换后的json，如果json中不包含被替换的key，返回None
        :param key:
        :param value:
        :return:
        """
        if not self.is_contained_the_key(key):
            return None
        json_d = self.__json
        point_key = PointKey(key)
        try:
            while point_key.size() > 1:
                k = point_key.next()
                if type(k) != int:
                    # 判断待处理的数据是否是列表
                    if type(json_d) is list:
                        json_d = json_d[0]
                json_d = json_d[k]
            k = point_key.next()
            json_d[k] = value
        except Exception:
            return None
        return self.to_good_json_str(self.__json)

    def delete_value(self, key):
        """
        得到删除key后的json，如果该key不存在，则返回None
        :param key:
        :return:
        """
        if not self.is_contained_the_key(key):
            return None
        json_d = self.__json
        point_key = PointKey(key)
        try:
            while point_key.size() > 1:
                k = point_key.next()
                if type(k) != int:
                    # 判断待处理的数据是否是列表
                    if type(json_d) is list:
                        json_d = json_d[0]
                json_d = json_d[k]
            k = point_key.next()
            del json_d[k]
        except Exception:
            return None
        return self.to_good_json_str(self.__json)

    def insert_value(self, key, value):
        """
        得到插入的key后的json，如果该key不存在，则返回None
        :param key:
        :param value:
        :return:
        """
        i_json = self.__json
        point_key = PointKey(key)
        try:
            while point_key.size() > 1:
                k = point_key.next()
                if type(k) != int:
                    # 如果待处理的key不是索引
                    # 判断待处理的数据是否是列表
                    if type(i_json) is list:
                        i_json = i_json[0]
                    v = i_json.get(k)
                    if point_key.is_index_next_key():
                        if type(v) != list:
                            i_json[k] = list()
                    else:
                        if type(v) != dict:
                            i_json[k] = dict()
                else:
                    if k >= len(i_json):
                        # 当k的值大于i_json的本来值时，使用追加
                        if point_key.is_index_next_key():
                            i_json.append(list())
                        else:
                            i_json.append(dict())
                        k = len(i_json) - 1
                    else:
                        v = i_json[k]
                        if point_key.is_index_next_key():
                            if type(v) != list:
                                i_json[k] = list()
                        else:
                            if type(v) != dict:
                                i_json[k] = dict()
                i_json = i_json[k]
            k = point_key.next()
            if type(k) != int:
                i_json[k] = value
            else:
                if k >= len(i_json):
                    i_json.append(value)
                else:
                    i_json[k] = value
        except Exception:
            return None
        return self.to_good_json_str(self.__json)


if __name__ == '__main__':
    print(JsonParse('{"a":1}').insert_value("a[1][1][1]", 1))
