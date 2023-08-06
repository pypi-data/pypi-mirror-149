# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: DB ,
"""
import importlib
import importlib.util
import re
from ..cfg.config import config
from ...exception.my_exception import MyException


class DBRes(object):
    def __init__(self, res, type_):
        self.__res = res
        if type_ == "select":
            self.__rows = len(self.__res)
            self.__columns = 0
            if type(self.__res) in [list, tuple]:
                if len(self.__res) > 0:
                    t = self.__res[0]
                    if type(t) in [list, tuple]:
                        self.__columns = len(t)
        else:
            self.__rows = self.__res
            self.__columns = 0

    @property
    def res(self):
        if type(self.__res) in [list, tuple] and len(self.__res) == 0:
            return [[]]
        return self.__res

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns


class DB(object):
    __db_info_re = re.compile(r"^/(mysql|oracle)/([^/\s]*)/([^/\s]*)/([^/\s:]*):?([0-9]*)?/([^/\s]*)$")

    def __init__(self, db_info: str):
        """
        db_config：/数据库类型/用户名/密码/地址[:端口]/数据库名或服务名
        :param db_info:
        """
        self.__software = None
        self.__username = None
        self.__password = None
        self.__server = None
        self.__port = None
        self.__conn = None
        self.__service_name = None
        self.__db_info = db_info
        self.__res = None
        if self.__db_info is None:
            raise MyException("未配置数据库信息，请检查！")
        if not self.is_the_db_info_correct(self.__db_info):
            raise MyException(
                "数据库db_info配置有误，正确的配置格式应是'/mysql|oracle/用户名/密码/地址[:端口]/服务名或数据库名'，而不是:{}".format(db_info))
        # 从数据库字符串里提取数据库连接信息
        self.__extract_db_info()

    @classmethod
    def is_the_db_info_correct(cls, db_info: str):
        """
        测试db_info字符串是否正确
        :return:
        """
        return cls.__db_info_re.match(db_info) is not None

    def connect(self):
        """
        连接到数据库
        """
        if self.__conn:
            return
        if self.__software == "mysql":
            self.__connect_fro_mysql()
        elif self.__software == "oracle":
            self.__connect_for_oracle()
        else:
            raise MyException("不支持对此类数据库的操作：{}".format(self.__software))

    def __connect_fro_mysql(self):
        if importlib.util.find_spec("pymysql") is None:
            raise MyException("要访问和操作mysql数据库，请安装PyMySQL==0.9.3!")
        pymysql = importlib.import_module("pymysql")
        server = self.__server
        port = self.__port
        if port is None:
            port = 3306
        user = self.__username
        passwd = self.__password
        database = self.__service_name
        # 连接数据库
        conn_error = None
        try:
            self.__conn = pymysql.connect(host=server, port=port, user=user, passwd=passwd, database=database)
        except pymysql.err.ProgrammingError as e:
            conn_error = str(e)
        except pymysql.err.InterfaceError as e:
            conn_error = str(e)
        except pymysql.err.OperationalError as e:
            conn_error = str(e)
        finally:
            if conn_error is not None:
                raise MyException("连接mysql数据库错误，提示：{}".format(conn_error))

    def __connect_for_oracle(self):
        if importlib.util.find_spec("cx_Oracle") is None:
            raise MyException("要访问和操作oracle数据库，请安装cx-Oracle==7.1.1！")
        cx_Oracle = importlib.import_module("cx_Oracle")
        if self.__port:
            server = "{server}:{port}".format(server=self.__server, port=self.__port)
        else:
            server = "{server}".format(server=self.__server)
        database_url = "{username}/{password}@{server}/{service_name}".format(username=self.__username,
                                                                              password=self.__password,
                                                                              server=server,
                                                                              service_name=self.__service_name)
        # 连接数据库
        conn_error = None
        try:
            self.__conn = cx_Oracle.connect(database_url)
        except cx_Oracle.DatabaseError as e:
            e = str(e)
            if "Cannot locate a 64-bit Oracle Client library" in e:
                conn_error = 1
            elif "Connect timeout occurred" in e:
                conn_error = 2
            elif "but version 11.2 or " in e:
                conn_error = 3
            else:
                raise
        except UnicodeDecodeError:
            conn_error = 1
        finally:
            if conn_error == 1:
                raise MyException("python连接oracle的环境未配置正确，请检查！可访问 http://172.32.4.219/docs/html/疑难问题解决指引/数据库相关.html#pythonoracle 寻求解决方案")
            elif conn_error == 2:
                raise MyException("连接数据库超时，请检查连接配置是否正确：{}".format(self.__db_info))
            elif conn_error == 3:
                raise MyException("oracle数据库版本不正确，请检查！")

    def close(self):
        """
        断开连接
        """
        if self.__conn is None:
            return
        self.__conn.close()
        self.__conn = None

    def __extract_db_info(self):
        """
        从db_info提取数据库信息
        :return:
        """
        # 用正在判断db_info字符串是否符合规范
        if not self.is_the_db_info_correct(self.__db_info):
            return None
        # 符合规范时提取相关信息
        # 提取所有信息
        db_info_l = self.__db_info_re.findall(self.__db_info)[0]
        # 取信息
        self.__software = db_info_l[0]
        self.__username = db_info_l[1]
        self.__password = db_info_l[2]
        self.__server = db_info_l[3]
        self.__port = int(db_info_l[4]) if db_info_l[4] != "" else None
        self.__service_name = db_info_l[5]

    def execute(self, sql: str) -> DBRes:
        """
        执行sql
        :return:
        """
        # 先检查sql是否符合测试要求
        self.check_sql(sql)
        # 连接数据库
        self.connect()
        # 调用对应的执行器
        if self.__software == "mysql":
            self.__execute_for_mysql(sql)
        elif self.__software == "oracle":
            self.__execute_for_oracle(sql)
        else:
            raise MyException("不支持对此类数据库的操作：{}".format(self.__software))
        return self.__res

    def __execute_for_mysql(self, sql: str):
        """
        执行mysql
        :param sql:
        :return:
        """
        self.__res = None
        sql_temp = sql.strip()
        cursor_error = None
        cursor = None
        try:
            # 获得游标
            cursor = self.__conn.cursor()
            # 执行sql
            cursor.execute(sql_temp)
            # 解析结果
            self.__resolve_res(cursor, sql)
            # 当为非查询语句时，修改记录大于指定值时，记录将回归
            if not self.is_a_query_statement(sql):
                max_ = config.get_config("max_number_non_select_sql",int)
                rows = cursor.rowcount
                if rows > max_:
                    raise MyException(
                        '''执行sql语句出错，单个非查询语句最大操作记录不能超过[{}],当前sql语句共修改了[{}]条记录，此次执行将会回滚。
此sql语句为:{}
最大操作记录请在config文件内配置【max_number_non_select_sql项】。'''.format(
                            max_, rows, sql))
        except Exception as e:
            # todo:后期需要修改这里，mysql是不会抛出这样的错误的
            cursor_error = str(e)
            self.__conn.rollback()
        except Exception:
            self.__conn.rollback()
            raise
        else:
            self.__conn.commit()
        finally:
            if cursor:
                cursor.close()
            if cursor_error:
                raise MyException("执行sql语句出错，数据库返回错误信息为：{}\n此sql语句为：{}".format(cursor_error, sql))

    def __execute_for_oracle(self, sql: str):
        """
        执行oracle数据库
        :return:
        """
        cx_Oracle = importlib.import_module("cx_Oracle")
        self.__res = None
        sql_temp = sql.strip()
        cursor_error = None
        cursor = None
        try:
            # 获得游标
            cursor = self.__conn.cursor()
            # 执行sql
            cursor.execute(sql_temp)
            # 解析结果
            self.__resolve_res(cursor, sql)
            # 当为非查询语句时，修改记录大于指定值时，记录将回归
            if not self.is_a_query_statement(sql):
                max_ = config.get_config("max_number_non_select_sql",int)
                rows = cursor.rowcount
                if rows > max_:
                    raise MyException(
                        '''执行sql语句出错，单个非查询语句最大操作记录不能超过[{}],当前sql语句共修改了[{}]条记录，此次执行将会回滚。
此sql语句为:{}
最大操作记录请在config文件内配置【max_number_non_select_sql项】。'''.format(
                            max_, rows, sql))
        except cx_Oracle.DatabaseError as e:
            cursor_error = str(e)
            self.__conn.rollback()
        except Exception:
            self.__conn.rollback()
            raise
        else:
            self.__conn.commit()
        finally:
            if cursor:
                cursor.close()
            if cursor_error:
                raise MyException("执行sql语句出错，数据库返回错误信息为：{}\n此sql语句为：{}".format(cursor_error, sql))

    def __resolve_res(self, cursor, sql):
        """
        解析结果
        :param cursor:
        :return:
        """
        if self.is_a_query_statement(sql):
            self.__res = DBRes(cursor.fetchall(), "select")
        else:
            # 非查询语句获取行数
            self.__res = DBRes(cursor.rowcount, "non-select")

    @classmethod
    def check_sql(cls, sql):
        """
        sql需符合以下要求
        1、只能执行select、insert、delete、update
        2、执行非查询语句时需至少带一个where字句，以防止修改整张表
        :param sql:
        :return:
        """
        if sql is None or sql == "":
            raise MyException("sql语句不能为空！")
        sql_temp = sql.lower().strip()
        if not (sql_temp.startswith("select") or sql_temp.startswith("insert") or sql_temp.startswith(
                "delete") or sql_temp.startswith("update")):
            raise MyException("sql语句执行只支持增删改查，不支持其他操作，请检查此语句：{}".format(sql))
        if (sql_temp.startswith("delete") or sql_temp.startswith("update")) and "where" not in sql_temp:
            raise MyException("sql语句执行非查询语句时必须至少带一个where字句，防止修改整张表，此sql语句未带字句，请检查:{}".format(sql))

    @classmethod
    def is_a_query_statement(cls, sql: str):
        """
        判断sql是否是查询语句，如果是，返回True，反正返回false
        :return:
        """
        cls.check_sql(sql)
        sql = sql.lower().strip()
        if sql.startswith("select"):
            return True
        else:
            return False
