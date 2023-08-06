# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: interface MyException
"""
from .my_exception import MyException
from ..function.track.xml_track import xmlTrack


class InfNameIsNullException(MyException):
    def __init__(self):
        tag=xmlTrack.current_tag()
        super(InfNameIsNullException, self).__init__(" {} 标签的name不能为空！".format(tag))


class InfFileNameIsIncorrectException(MyException):
    def __init__(self, error_name):
        tag=xmlTrack.current_tag()
        msg=" {} 标签的name {} 是不正确的,不是正则表达式或$whole！".format(tag,error_name)
        super(InfFileNameIsIncorrectException, self).__init__(msg)


class InfPortAndServerNameIsIncorrectException(MyException):
    def __init__(self, error_name):
        tag=xmlTrack.current_tag()
        msg=" {} 标签的name {} 是不正确的,只能是$whole".format(tag, error_name)
        super(InfPortAndServerNameIsIncorrectException, self).__init__(msg)


class InfActIsIncorrectException(MyException):
    def __init__(self, error_act):
        tag=xmlTrack.current_tag()
        msg=" {} 标签的act {} 是不正确的，只能是delete,replace,insert".format(tag, error_act)
        super(InfActIsIncorrectException, self).__init__(msg)


class InfValueIsNotNoneException(MyException):
    def __init__(self, act, name):
        if name == "$Regex":
            name = "正则表达式"
        tag=xmlTrack.current_tag()
        msg="{}标签的act是{}时，其标签值不能为空!".format(tag,act)
        super(InfValueIsNotNoneException, self).__init__(msg)


class InfDataIsNotMatchedException(MyException):
    def __init__(self, scope, regex, inf_name, inf_data):
        tag=xmlTrack.current_tag()
        msg="{} 标签处理出错，接口 {} 的 {} 与 正则表达式 {} 匹配失败\n待匹配字符串为 {}".format(tag,inf_name,scope,regex,inf_data)
        super(InfDataIsNotMatchedException, self).__init__(msg)


class InfDataNotContainsTheWellException(MyException):
    def __init__(self, scope, well, inf_name, inf_data):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，接口 {} 的 {} 中 {} 不包含 {} ".format(tag, inf_name, scope, inf_data, well)
        super(InfDataNotContainsTheWellException, self).__init__(msg)

class InfDataNotSupportException(MyException):
    def __init__(self, scope, inf_name, act):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，接口 {} 的 {} 不支持name为#表达式进行 {} 动作 ".format(tag, inf_name, scope, act)
        super(InfDataNotSupportException, self).__init__(msg)

class InfIsNotFileException(MyException):
    def __init__(self, inf_name):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，接口 {} 不是一个文件上传接口！".format(tag, inf_name)
        super(InfIsNotFileException, self).__init__(msg)

class InfReTypeIsUnsupportedException(MyException):
    def __init__(self, ty):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，不支持对类型为 {} 的数据进行处理！".format(tag, ty)
        super(InfReTypeIsUnsupportedException, self).__init__(msg)


class InfDataIsNotFindException(MyException):
    def __init__(self, scope, key, inf_name):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，接口 {} 的 {} 不存在关键字 {} 或关键字格式错误".format(tag, inf_name, scope, key)
        super(InfDataIsNotFindException, self).__init__(msg)

class InfDataIsIncorrectException(MyException):
    def __init__(self, scope, inf_name):
        tag=xmlTrack.current_tag()
        msg=" {} 标签处理出错，接口 {} 的 {} 格式不正确，请检查！".format(tag, inf_name, scope)
        super(InfDataIsIncorrectException, self).__init__(msg)

class InfInsertFailException(MyException):
    def __init__(self, scope, inf_name, insert_key, value):
        tag=xmlTrack.current_tag()
        msg= "{} 标签处理出错，在接口 {} 的 {} 中插入参数 {} 失败，因为参数格式不正确，其待插入的值为 {}".format(tag, inf_name, scope, insert_key,value)
        super(InfInsertFailException, self).__init__(msg)
