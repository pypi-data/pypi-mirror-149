# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: post processor MyException
"""
from .my_exception import MyException
from ..function.track.xml_track import xmlTrack


class PostTypeIsIncorrectException(MyException):
    def __init__(self, error_type: str) -> None:
        tag = xmlTrack.current_tag()
        msg = "{}标签处理器不支持此type:{}".format(tag, error_type)
        super(PostTypeIsIncorrectException, self).__init__(msg)


class PostDescIsNullException(MyException):
    def __init__(self) -> None:
        tag = xmlTrack.current_tag()
        super(PostDescIsNullException, self).__init__("{}标签的desc不能为空！".format(tag))


class PostKeyTypeIsIncorrectException(MyException):
    def __init__(self, key: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签的key错误,当结果类型是二维表数据时,key应是数字切片的格式,类似'1:2',不应是:{}！".format(tag, key)
        super(PostKeyTypeIsIncorrectException, self).__init__(msg)


class PostActIsIncorrectException(MyException):
    def __init__(self, act: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签的act错误,不能是:{}!".format(tag, act)
        super(PostActIsIncorrectException, self).__init__(msg)


class PostVarTypeIsNotSupportException(MyException):
    def __init__(self, type_: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签的var_type不受支持,不能是:{}".format(tag, type_)
        super(PostVarTypeIsNotSupportException, self).__init__(msg)


class PostNameIsNotSupportedException(MyException):
    def __init__(self, name: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签的name不符合规则,只能以字母下划线开头且只包含字母数字下划线,不能是:{}".format(tag, name)
        super(PostNameIsNotSupportedException, self).__init__(msg)


class PostNameIsNullException(MyException):
    def __init__(self):
        tag = xmlTrack.current_tag()
        msg = "{}标签的name不能是空!".format(tag)
        super(PostNameIsNullException, self).__init__(msg)


class PostValueIsNotSpecifiedException(MyException):
    def __init__(self):
        tag = xmlTrack.current_tag()
        msg = "{}标签的value或type未指定！".format(tag)
        super(PostValueIsNotSpecifiedException, self).__init__(msg)


class PostSqlIsNotSpecifiedException(MyException):
    def __init__(self):
        tag = xmlTrack.current_tag()
        msg = "{}标签未配置sql语句!".format(tag)
        super(PostSqlIsNotSpecifiedException, self).__init__(msg)


class PostExpressIsIncorrectException(MyException):
    def __init__(self, error: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签的ex属性指定的表达式计算出错，错误原因时为:{}".format(tag, error)
        super(PostExpressIsIncorrectException, self).__init__(msg)


class PostNotFindValueException(MyException):
    def __init__(self, res_type: str, key: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签未在结果 {} 中找到关键字为 {} 或关键字格式不正确".format(tag, res_type, key)
        super(PostNotFindValueException, self).__init__(msg)


class PostReTypeIsNotSupportedException(MyException):
    def __init__(self, re_type: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签不支持处理此种类型的结果:{}".format(tag, re_type)
        super(PostReTypeIsNotSupportedException, self).__init__(msg)


class PostReqDataIsNullException(MyException):
    def __init__(self):
        tag = xmlTrack.current_tag()
        msg = "{}标签无法处理请求报文，因为该接口的请求报文为空!".format(tag)
        super(PostReqDataIsNullException, self).__init__(msg)


class PostSleepValueIsNotNumberException(MyException):
    def __init__(self, value: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签传入的结果值必须一个数字，而不是：{}".format(tag, value)
        super(PostSleepValueIsNotNumberException, self).__init__(msg)


class PostTransferFailException(MyException):
    def __init__(self, value: str, type_: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签取到的数据 {} 不是 {} 类型，转型失败!".format(tag, value, type_)
        super(PostTransferFailException, self).__init__(msg)


class PostValueAndExceptValueIsNotSameException(MyException):
    def __init__(self, real: str, except_v: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签取到的值 {} 与value属性说明的值 {} 不一致！".format(tag, real, except_v)
        super(PostValueAndExceptValueIsNotSameException, self).__init__(msg)


class PostValueAndExceptValueIsNotMatchedException(MyException):
    def __init__(self, real: str, regex: str):
        tag = xmlTrack.current_tag()
        msg = "{}标签取到的值 {} 与处理器value说明的正则表达式 {} 不匹配!".format(tag, real, regex)
        super(PostValueAndExceptValueIsNotMatchedException, self).__init__(msg)


class PostValueTypeIsNotCorrectException(MyException):
    def __init__(self, value, _type):
        tag = xmlTrack.current_tag()
        msg = "{}标签取到的值 {} 类型 {} 不正确，当需要设置多个变量时，值的类型必须是列表或tuple!".format(tag, value, _type)
        super(PostValueTypeIsNotCorrectException, self).__init__(msg)


class PostValueLengthIsNotCorrectException(MyException):
    def __init__(self, need_length, real_length):
        tag = xmlTrack.current_tag()
        msg = "{}标签需要的变量数:{}个与实际得到的变量数:{}个不等!".format(tag, need_length, real_length)
        super(PostValueLengthIsNotCorrectException, self).__init__(msg)
