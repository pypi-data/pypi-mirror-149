# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: parse test data xml file and all api xml file
"""
from .flow import FlowDict
from .interface import InterfaceDict
from .test_data import ParserTestData

interface = InterfaceDict()
flow = FlowDict()
ParserTestData = ParserTestData
