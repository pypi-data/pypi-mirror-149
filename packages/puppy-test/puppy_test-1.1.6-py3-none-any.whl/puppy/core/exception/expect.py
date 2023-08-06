# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: expect exception
"""
from .my_exception import MyException


class ExpectDescIsNullException(MyException):
    def __init__(self) -> None:
        super(ExpectDescIsNullException, self).__init__("期望标签的描述不能为空！")


class ExpectKeyTypeIsIncorrectException(MyException):
    def __init__(self, key: str):
        msg = "期望标签的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{}".format(key)
        super(ExpectKeyTypeIsIncorrectException, self).__init__(msg)


class ExpectActIsNullException(MyException):
    def __init__(self) -> None:
        msg = "期望标签未指定指定act属性!"
        super(ExpectActIsNullException, self).__init__(msg)


class ExpectSqlIsNullException(MyException):
    def __init__(self) -> None:
        msg="期望标签的type为sql时，必须指定要执行的sql语句！"
        super(ExpectSqlIsNullException, self).__init__(msg)


class ExpectValueIsNullException(MyException):
    def __init__(self) -> None:
        super(ExpectValueIsNullException, self).__init__("期望标签未指定期望值!")


class ExpectTypeIsUnsupportedException(MyException):
    def __init__(self, type_):
        msg="期望标签的type属性不正确，不支持：{}".format(type_)
        super(ExpectTypeIsUnsupportedException, self).__init__(msg)


class ExpectReTypeUnsupportedException(MyException):
    def __init__(self, type_):
        msg="期望标签不支持对 {} 类型的结果进行处理".format(type_)
        super(ExpectReTypeUnsupportedException, self).__init__(msg)


class ExpectJsonException(MyException):
    def __init__(self, error_json: str):
        msg="期望标签处理的数据不是正确的json格式字符串：{}".format(error_json)
        super(ExpectJsonException, self).__init__(msg)


class ExpectActIsUnsupportedException(MyException):
    def __init__(self, act: str):
        msg="期望标签不支持此act属性:{}".format(act)
        super(ExpectActIsUnsupportedException, self).__init__(msg)


class ExpectTagOfValueIsNullException(Exception):
    def __init__(self):
        super(ExpectTagOfValueIsNullException, self).__init__("期望标签的type是expression时，其value不能为空!")
