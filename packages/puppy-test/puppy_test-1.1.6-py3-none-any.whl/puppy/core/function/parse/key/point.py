# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: is key of type of point
"""
import re


class PointKey(object):
    __split_key_from_str_re = re.compile(r"(?<!\\)\.")
    __extract_from_key_re = re.compile(r"^(?P<name>.+?)((?<!\\)\[(\d+)])+$")
    __extract_index_re = re.compile(r"\d+")
    __special_root = "$__root__"

    def __init__(self, key_str):
        """
        此类用来解析key字符串为.连接的键
        """
        self.__start_by_index = False
        self.__key_str = self.__process_key(key_str)
        self.__key_list = None
        self.__keys = None

    def __process_key(self, key_str):
        """
        如果key是索引开始的，附加上一个特殊开头，并将start_ty_index标志位置为true
        :param key_str:
        :return:
        """
        if key_str[0] == "[":
            self.__start_by_index = True
            return "{}{}".format(self.__special_root, key_str)
        return key_str

    def next(self):
        """
        弹出一个key
        return:
        """
        if self.__key_list is None:
            self.__extract_key_from_str()
        if self.__keys is None:
            self.__extract_key_details()
        return self.__keys.pop(0)

    def has(self):
        """
        如果有下一个则返回None
        """
        if self.__key_list is None:
            self.__extract_key_from_str()
        if self.__keys is None:
            self.__extract_key_details()
        return len(self.__keys) != 0

    def size(self):
        """
        返回list的数量
        """
        if self.__key_list is None:
            self.__extract_key_from_str()
        if self.__keys is None:
            self.__extract_key_details()
        return len(self.__keys)

    def is_index_next_key(self) -> bool:
        """
        下一个key是索引吗
        """
        if self.__key_list is None:
            self.__extract_key_from_str()
        if self.__keys is None:
            self.__extract_key_details()
        return len(self.__keys) > 0 and type(self.__keys[0]) == int

    def __extract_key_from_str(self):
        """
        从key字符串中分隔key
        """
        if self.__key_str is None:
            self.__key_list = list()
        key_list = self.__split_key_from_str_re.split(self.__key_str)
        while key_list.count("") > 0:
            key_list.remove("")
        self.__key_list = key_list

    def __extract_key_details(self):
        """
        提取key的细节
        """
        self.__keys = []
        for key in self.__key_list:
            # 把\.转为.
            key = key.replace(r"\.", ".")
            # 从key中提取数字
            matcher = self.__extract_from_key_re.match(key)
            if matcher:
                name = matcher.group("name")
                # 如果start_by_index为真，则不添加次name到key列表
                if self.__start_by_index:
                    self.__start_by_index = False
                else:
                    # 把\[和\]替换为[和]
                    name = name.replace(r"\[", "[").replace(r"\]", "]", re.M)
                    self.__keys.append(name)
                left, right = matcher.span("name")
                index_str = key[right:]
                index_list = self.__extract_index_re.findall(index_str)
                for x in index_list:
                    self.__keys.append(int(x))
            else:
                name = key.replace(r"\[", "[").replace(r"\]", "]")
                self.__keys.append(name)


if __name__ == '__main__':
    print(PointKey("a[1][1][2]").next())
