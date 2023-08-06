# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: SQL client
"""
from .client import AbstractClient
from ....data.interface import Interface
from ....exception.my_exception import MyException
from ....function.database.db import DB
from ....function.parse.json_parse import JsonParse
from ....function.parse.table_parse import TableParse
from ....function.thread.pool import ResourcePool
from ....printer.format_printer import Printer


class SQL(AbstractClient):
    """
    SQL客户端
    """

    def __init__(self, interface_info: Interface, interface_data: dict, context: dict):
        """
        SQL客户端
        :param interface_info:接口信息
        :param interface_data: 接口数据
        :param context: 场景上下文
        :return:
        """
        super().__init__(interface_info, interface_data, context)

    def _request(self):
        # 构造数据库连接字符串
        # 从请求头中提取相关信息
        header = JsonParse.to_json(self._interface_info.header)
        type_ = header.get("type")
        user = header.get("user")
        password = header.get("password")
        database = header.get("database")
        if type_ is None or user is None or password is None or database is None:
            raise MyException('''请求的SQL接口的头格式不正确，正确的格式应为：
        {
            "type":"oracle|mysql",
            "user":"user",
            "password":"password",
            "database":"database"
        }''')
        if type_ not in ["oracle", "mysql"]:
            raise MyException("SQL接口目前仅支持[oracle][mysql]，不支持{}".format(type_))
        port = self._interface_info.port
        server = self._interface_info.server
        sql = self._interface_info.body
        # 构造一个链接url db_config：/数据库类型/用户名/密码/地址[:端口]/数据库名或服务名
        if port is None:
            db_config = "/{}/{}/{}/{}/{}".format(type_, user, password, server, database)
        else:
            db_config = "/{}/{}/{}/{}:{}/{}".format(type_, user, password, server, port, database)
        # 发送一个sql请求
        p_port = "" if port is None else port
        header["password"]="******"
        Printer.print_request_info("SQL", self._interface_info.desc, "{}:{}".format(server, p_port), header, sql,
                                   "sql")
        if not DB.is_the_db_info_correct(db_config):
            raise MyException(
                "数据库db_info配置有误，正确的配置格式应是'/mysql|oracle/用户名/密码/地址[:端口]/服务名或数据库名'，而不是:{}".format(db_config))
        result = ResourcePool().exec_sql(db_config, sql)
        self._res.text = result.res
        self._res.code = 400
        # 判断sql语句是查询语句吗
        if DB.is_a_query_statement(sql):
            self._res.re_type = "table"
            self._res.text = TableParse.tuple_to_list(self._res.text)
        else:
            self._res.re_type = "number"
        Printer.print_response_info("SQL", self._res)
