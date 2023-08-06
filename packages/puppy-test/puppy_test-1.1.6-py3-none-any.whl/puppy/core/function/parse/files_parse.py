# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: is used to process files
"""


class Files(object):

    def __init__(self, files: dict):
        self.__files = files

    @classmethod
    def is_file_interface(cls, files):
        return files is not None

    def is_exists(self, name):
        """
        判断此name是否存在于文件域
        """
        for key, value in self.__files.items():
            if name == key:
                return True
        return False

    def replace_value(self, name, value):
        """
        替换name指定的文件内容
        """
        if not self.is_exists(name):
            return None
        if value is None:
            return self.remove_value(name)
        one_file = self.__files[name]
        new_file = (value, one_file[1])
        self.__files[name] = new_file
        return self.__files

    def insert_value(self, name, value):
        """
        插入一个新的file
        """
        if value is not None:
            self.__files[name] = (value, "multipart/form-data")
        return self.__files

    def remove_value(self, name):
        """
        删除一个file
        """
        if not self.is_exists(name):
            return None
        self.__files.pop(name)
        return self.__files
