# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: type of table data
"""
from ..utils.utils import Utils
from ...exception.my_exception import MyException


class TableParse(object):

    def __init__(self, table):
        """
        表格类型的数据，即二维数据，暂时只支持[()]或([])或(())或[[]]，其他类型的二维表示形式待以后再根据情况支持
        :param table:
        """
        if type(table) not in [list, tuple]:
            raise MyException("不是受支持的表格数据:{}".format(str(table)))
        self.__table = table

    @classmethod
    def check_key(cls, key):
        """
        检查key是否正确，如果不正确，则返回False
        用来取表格数据的key应该是由2个数字组成，格式为'1,2',第一个数字指明取多少行，第二个数字指明取多少列，从0开始计算
        :return:
        """
        try:
            cls.extract_key(key)
            return True
        except Exception:
            return False

    def get_value(self, key: str):
        """
        获得表格中key指定的数据，如果key错误，或者未取到返回错误标志
        :param key:
        :return:
        """
        try:
            row_1, row_2, column_1, column_2 = TableParse.extract_key(key)
            res = self.__extract_data(self.__table, row_1, row_2, column_1, column_2)
            res = TableParse.tuple_to_list(res)
            return res
        except Exception:
            return Utils.ERROR

    @staticmethod
    def __extract_data(table, row1, row2, column1, column2):
        if row1 == "#":
            row1 = 0
        if column1 == "#":
            column1 = 0
        if row1 is not None and column1 is not None and row2 is None and column2 is None:
            return table[row1][column1]
        if row1 is not None and row2 is not None and column1 is not None and column2 is None:
            if row2 == "#":
                row2 = len(table)
            rows = table[row1:row2]
            res = list()
            for row in rows:
                res.append(row[column1])
            return res
        if row1 is not None and column1 is not None and column2 is not None and row2 is None:
            rows = table[row1]
            if column2 == "#":
                column2 = len(rows)
            return rows[column1:column2]
        if row1 is not None and row2 is not None and column1 is not None and column2 is not None:
            if row2 == "#":
                row2 = len(table)
            rows = table[row1:row2]
            res = list()
            for row in rows:
                if column2 == "#":
                    column2 = len(row)
                res.append(row[column1:column2])
            return res

    @classmethod
    def tuple_to_list(cls, data):
        """
        将数据结构中的元祖转为列表，浮点数转为decimal浮点数
        :param data:
        :return:
        """
        if type(data) in [list, tuple]:
            temp = list()
            for d in data:
                temp.append(cls.tuple_to_list(d))
            return temp
        else:
            return data

    @staticmethod
    def extract_key(key_str):
        """
        提取行和列,#代表取到最小和最大值，None代表此值未有
        :param key:
        :return:
        """
        if key_str.count("#") > 0:
            raise MyException("key表达式格式错误！")
        row1 = "#"
        row2 = "#"
        column1 = "#"
        column2 = "#"
        key_str = key_str.replace(" ", "")
        if key_str == "$whole":
            return row1, row2, column1, column2
        keys = key_str.split(",")
        keys_len = len(keys)
        if keys_len == 1:
            # 仅有行
            row_str = keys[0]
            rows = row_str.split(":")
            rows_len = len(rows)
            if rows_len == 1:
                # 仅有row1
                if rows[0] == "":
                    raise MyException("行号不可以为空！")
                row1 = int(rows[0])
                row2, column1, column2 = None, "#", "#"
            elif rows_len == 2:
                if rows[0] == "":
                    row1 = "#"
                else:
                    row1 = int(rows[0])
                if rows[1] == "":
                    row2 = "#"
                else:
                    row2 = int(rows[1])
            else:
                raise MyException("行号格式错误！")
            return row1, row2, column1, column2
        elif len(keys) == 2:
            row_str = keys[0]
            column_str = keys[1]
            rows = row_str.split(":")
            rows_len = len(rows)
            if rows_len == 1:
                # 仅有row1
                if rows[0] == "":
                    raise MyException("行号不可以为空！")
                else:
                    row1 = int(rows[0])
                row2 = None
            elif rows_len == 2:
                if rows[0] == "":
                    row1 = "#"
                else:
                    row1 = int(rows[0])
                if rows[1] == "":
                    row2 = "#"
                else:
                    row2 = int(rows[1])
            else:
                raise MyException("行号格式错误！")
            columns = column_str.split(":")
            column_len = len(columns)
            if column_len == 1:
                # 仅有column1
                if columns[0] == "":
                    raise MyException("列号不可以为空！")
                column1 = int(columns[0])
                column2 = None
            elif column_len == 2:
                if columns[0] == "":
                    column1 = "#"
                else:
                    column1 = int(columns[0])
                if columns[1] == "":
                    column2 = "#"
                else:
                    column2 = int(columns[1])
            else:
                raise MyException("列号不可以为空！")
            return row1, row2, column1, column2
        else:
            raise MyException("提取表达式错误！")

