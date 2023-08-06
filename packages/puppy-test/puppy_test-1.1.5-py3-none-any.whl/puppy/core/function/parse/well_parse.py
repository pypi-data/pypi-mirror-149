# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: is used to process #{}
"""


class WellParse(object):

    def __init__(self,original:str):
        """
        源字符串
        :param o:
        """
        self.__original=str(original)

    @classmethod
    def is_well(cls,name:str):
        """
        判断是否是#字符name
        :param name:
        :return:
        """
        if len(name)<=3:
            return False
        if name[0]=="#" and name[-1]=="}" and name[1]=="{":
            return True
        return False

    def replace_value(self, name, value):
        """
        :param name:
        :param value:
        :return:
        """
        if name not in self.__original:
            return None
        return self.__original.replace(name,value)
