# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:read test data xml
"""

import os
import re

from .. import config
from ..exception.my_exception import MyException
from ..function.express.express import Express
from ..function.track.xml_track import xmlTrack
from ..function.utils.utils import Utils
from ..function.analysis.xml_parser import XmlParser


class ParserTestData(object):
    __auto_xml_file_re = re.compile(
        r"^test_\d+[a-zA-Z_\u4e00-\u9fa5，。；（）][a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*_\d+[a-zA-Z_\u4e00-\u9fa5，。；（）]["
        r"a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*\.xml$")

    __unit_xml_file_re = re.compile(
        r"^test_[a-zA-Z_\u4e00-\u9fa5，。；（）][a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*_[a-zA-Z_\u4e00-\u9fa5，。；（）]["
        r"a-zA-Z_\u4e00-\u9fa5，。；（）0-9]*\.xml$")

    __case_name_re = re.compile(r"^[a-zA-Z0-9_\u4e00-\u9fa5，。；：（）！、,!()+-]+$")

    def __init__(self, test_data_file: str, id_="-1"):
        """
        解析测试数据文件
        :param test_data_file: 文件路径
        :return: None
        """
        # 对传入的文件名进行判断，其格式必须为【test_模块编号模块名称_场景编号场景名称.xml】
        _type = config.get_config("the_global_inspection_type", str)
        if _type == "unit":
            if not self.__unit_xml_file_re.fullmatch(test_data_file):
                raise MyException("案例文件的命令必须符合以下规则：\n"
                                  "1、格式：test_模块名称_接口名称\n"
                                  "2、名称中只能包含字母数字下划线中文及部分中文符号，且不可以以数字开头\n"
                                  "当前案例文件命名不符合此规则，请检查对应的案例xml并修改：[{}]".format(test_data_file))
        else:
            if not self.__auto_xml_file_re.fullmatch(test_data_file):
                raise MyException("案例PY文件的命名必须符合以下规则：\n1、格式[test_模块编号模块名称_场景编号场景名称.py]\n"
                                  "2、模块和场景名称只能包含字母数字下划线中文及部分中文符号，且不可以以数字开头；\n"
                                  "当前执行的PY文件不符合此规则，请检查对应的案例xml并修改：[{}]".format(test_data_file))
        self.__test_data_file = os.path.join(config.get_config("test_data_path"), test_data_file)
        self.__test_data = None
        self.__id = id_

    def __parse_xml(self):
        """
        解析测试数据文件
        :return: None
        """
        if not os.path.exists(self.__test_data_file):
            raise MyException(
                "对应的数据xml文件[{}]不存在,请检查[{}]目录".format(self.__test_data_file, config.get_config("test_data_path")))
        root = XmlParser(self.__test_data_file).parse_xml()
        scene = root["scene"]
        cases = scene["case"]
        cases = cases if type(cases) == list else [cases]
        # 取得db_info
        db_info = Utils.extract_attrs_from_dict(scene, "db_info", "$value")
        # 取得工号
        author_work_number = Utils.extract_attrs_from_dict(scene, "author_work_number")
        author_work_number = None if author_work_number == "" else author_work_number
        # 如果db_info为空，取得全局的
        if db_info is None:
            # 如果全局的不为空，则对其进行计算
            if config.have_config('db_info'):
                db_info = Express.calculate_str(config.get_config('db_info'))
        else:
            # 计算db
            db_info = Express.calculate_str(db_info)
        real_cases = []
        count_of_cases = len(str(len(cases)))
        for case in cases:
            xmlTrack.push_source_data(case, "case")
            id_ = case.get("id")
            if self.__id != "-1" and self.__id != id_:
                continue
            if db_info is not None and case.get("db_info") is None:
                case["db_info"] = db_info
            elif case.get("db_info") is not None:
                case["db_info"] = Express.calculate_str(case["db_info"])
            name = case.get("name")
            if config.get_config("the_global_inspection", bool) and not self.__case_name_re.fullmatch(name) or len(
                    name) > 100:
                raise MyException(
                    "案例名称需符合以下规则：\n1、只能包含字母数字中文。\n2、只能包含中文/英文逗号，中文句号，中文冒号，中文分号，中文/英文括号，中文/英文感叹号，中文分号，加号，减号及下划线。\n3"
                    "、长度不能超过100个字符；\n此案例名：[{}]不符合此规则，请检查！".format(
                        name))
            case_author_work_number = Utils.extract_attrs_from_dict(scene, "author_work_number")
            case_author_work_number = None if case_author_work_number == "" else case_author_work_number
            if config.get_config("the_global_inspection_type", str) == "unit":
                if author_work_number is None and case_author_work_number is None:
                    raise MyException("单元测试案例的作者工号不可为空！请在案例XML的scene或case标签增加author_work_number属性并填写真实的工号。")
            real_cases.append(case)
            case["id"] = Utils.add_zero_to(case["id"], count_of_cases)
            xmlTrack.pop()
        self.__test_data = real_cases

    @property
    def test_data(self):
        if not self.__test_data:
            self.__parse_xml()
        return self.__test_data
