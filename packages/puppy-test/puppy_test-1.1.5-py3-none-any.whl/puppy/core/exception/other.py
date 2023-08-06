# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: if tag MyException
"""
from .my_exception import MyException
from ..function.track.xml_track import xmlTrack


class IFExpressIncorrectException(MyException):
    def __init__(self, error: str):
        tag=xmlTrack.current_tag()
        msg="{}标签的ex表达式计算错误，具体错误原因为:{}".format(tag,error)
        super(IFExpressIncorrectException, self).__init__(msg)

class IFDescIsNullException(MyException):
    def __init__(self):
        super(IFDescIsNullException, self).__init__("if标签的描述不能为空！")

class UnexpectedTagsException(MyException):
    def __init__(self):
        super(UnexpectedTagsException, self).__init__("存在不应存在的标签，请检查！")


class FileIsNotExistsException(MyException):
    def __init__(self, file):
        super(FileIsNotExistsException, self).__init__("文件上传接口中指定的文件：{} 不存在，请检查！".format(file))


class ReqDataIsIncorrectException(MyException):
    def __init__(self):
        super(ReqDataIsIncorrectException, self).__init__("请求报文格式不正确，请检查！")
