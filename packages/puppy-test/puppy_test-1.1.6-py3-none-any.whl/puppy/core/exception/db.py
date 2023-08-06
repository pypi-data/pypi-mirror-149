# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: db exception
"""
from .my_exception import MyException


class DBInformationIsNotConfiguredException(MyException):
    def __init__(self):
        super(DBInformationIsNotConfiguredException, self).__init__("未配置数据库连接信息,请检查配置文件或案例XML!")


class DBInformationIsIncorrectException(MyException):
    def __init__(self, error_db_info: str):
        super(DBInformationIsIncorrectException, self).__init__("数据库db_info配置有误，正确的配置格式应是:/mysql|oracle/用户名/密码/地址[:端口]/服务名或数据库名,而不是:{}".format(error_db_info))
