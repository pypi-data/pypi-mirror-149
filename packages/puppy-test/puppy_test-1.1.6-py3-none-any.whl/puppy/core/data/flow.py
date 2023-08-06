# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:read flow xml
"""

import os

from .. import config
from ..exception.my_exception import MyException
from ..function.analysis.xml_parser import XmlParser
from ..function.express.express import Express
from ..function.utils.utils import Utils


class ParserFlowData(object):
    def __init__(self, flow_file: str):
        """
        解析接口文件
        :return: None
        """
        self.__flow_file = flow_file
        self.__flow = None

    def __parse_xml(self):
        """
        解析接口文件
        :return: None
        """
        if not os.path.exists(self.__flow_file):
            raise MyException("流程XML文件[{}]不存在,请检查！".format(self.__flow_file))
        parsed_xml = XmlParser(self.__flow_file).parse_xml()
        self.__flow = parsed_xml["flow"]

    @property
    def flow(self):
        if not self.__flow:
            self.__parse_xml()
        return self.__flow


class Flow(object):
    def __init__(self, flow_name):
        """
        流程定义数据
        :param flow_name:流程的名字
        """
        # 取得流程名称
        self.__name = flow_name
        # 流程对应的文件
        self.__flow_file_path = os.path.join(config.get_config("flow_path"), "{}.xml".format(flow_name))
        # 取得流程的参数
        flow_data = ParserFlowData(self.__flow_file_path).flow
        # 取得参数
        self.__params, self.__content = Flow.__get_params(flow_data)

    @staticmethod
    def __get_params(flow_data: dict):
        """
        取得过程的参数列表
        :param flow_data:
        :return:
        """
        params = dict()
        content = dict()
        for key, value in flow_data.items():
            if key in ["xmlns", "xmlns:xsi", "xsi:schemaLocation"]:
                continue
            elif key in Utils.FLOW_INNER_TAG:
                content[key] = value
            else:
                params[key] = Express.calculate_str(value)
        return params, content

    @property
    def name(self):
        return self.__name

    @property
    def content(self):
        return self.__content

    @property
    def params(self):
        return self.__params


class FlowDict(object):
    def __init__(self):
        """
        用来存储所有的流程
        """
        self.__flow_dict = dict()

    def get(self, flow_name) -> Flow:
        """
        取到flow
        :param flow_name: 流程的名字
        :return:
        """
        if self.__flow_dict.get(flow_name) is None:
            # 读取flow
            self.__flow_dict[flow_name] = Flow(flow_name)
        return self.__flow_dict.get(flow_name)
