# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: response of client
"""
import re


class ResData(object):
    __xml_re = re.compile(r"<\w*>.*?</\w*>")
    __json_re = re.compile(r"{[\s\S]*?}")

    def __init__(self, response_code=-1, response_text="", response_header="",response_header_type=None):
        # 构建一个响应结果
        # 接口响应结果
        self.__response_code = response_code
        # 接口响应内容
        self.__response_text = response_text
        # 接口响应头
        self.__response_header = response_header
        # 推测响应结果类型
        self.__re_type = -1
        self.__response_header_type=response_header_type

    def __speculate_res_type(self):
        """
        推测响应结果类型
        json,xml
        """
        if self.__re_type == -1:
            res = str(self.__response_text)
            if "<html>" in res:
                self.__re_type = "html"
            elif ResData.__xml_re.match(res):
                self.__re_type = "xml"
            elif ResData.__json_re.match(res):
                self.__re_type = "json"
            else:
                self.__re_type = None
        return self.__re_type

    @property
    def re_type(self):
        return self.__speculate_res_type()

    @re_type.setter
    def re_type(self, re_type):
        self.__re_type = re_type

    @property
    def code(self):
        return self.__response_code

    @code.setter
    def code(self, code):
        self.__response_code = code

    @property
    def text(self):
        return self.__response_text

    @text.setter
    def text(self, text):
        self.__re_type = -1
        self.__response_text = text

    @property
    def header(self):
        return self.__response_header

    @header.setter
    def header(self, header):
        self.__response_header = header

    @property
    def header_type(self):
        return self.__response_header_type

    @header_type.setter
    def header_type(self,header_type):
        self.__response_header_type=header_type