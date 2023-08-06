# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: pre processor Exception
"""
from .my_exception import MyException


class HttpMethodIsNotSupportedException(MyException):
    def __init__(self, error_method):
        super(HttpMethodIsNotSupportedException, self).__init__("当前HTTP客户端不支持此请求方法：{}!".format(error_method))


class HttpDataIsNotSupportedException(MyException):
    def __init__(self, method, error_type):
        super(HttpDataIsNotSupportedException, self).__init__("当前HTTP客户端的 {} 方法无法处理 {} 格式的数据!".format(method, error_type))
