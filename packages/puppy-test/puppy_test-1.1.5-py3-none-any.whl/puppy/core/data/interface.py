# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:read all interfaces information
"""
import os
import re
from typing import Union

from ..exception.my_exception import MyException
from ..function.track.xml_track import xmlTrack
from ..function.utils.utils import Utils
from ..function.analysis.xml_parser import XmlParser
from ..function.cfg.config import config
from ..function.express.express import Express


class ParserInterfaceData(object):
    def __init__(self, interface_file: str):
        """
        解析接口文件
        :param interface_file:接口文件
        :return: None
        """
        self.__interface_file = interface_file
        self.__interface = None

    def __parse_xml(self):
        """
        解析接口文件
        :return: None
        """
        if not os.path.exists(self.__interface_file):
            raise MyException("接口定义XML文件[{}]不存在,请检查！".format(self.__interface_file))
        parsed_xml = XmlParser(self.__interface_file).parse_xml()
        self.__interface = parsed_xml["interface"]

    @property
    def interface(self):
        if not self.__interface:
            self.__parse_xml()
        return self.__interface


class Interface(object):
    __express_re = re.compile(r"\${(.*?)}")

    def __init__(self, interface_name):
        """
        :return:
        """
        # 接口名称
        self.__name = self.__get_correct_name(interface_name)
        # 构造接口文件
        interface_path = os.path.join(config.get_config("api_file_path"), "{}.xml".format(interface_name))
        # 读取接口信息
        interface_info = ParserInterfaceData(interface_path).interface
        xmlTrack.push_source_data(interface_info, "interface")
        # 接口描述
        self.__desc = self.__get_correct_desc(interface_info.get("desc"))
        # 接口协议
        self.__protocol = self.__get_correct_protocol(interface_info.get("protocol"))
        # 请求类型
        self.__method = self.__get_correct_method(interface_info.get("method"), self.__protocol)
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "path"), "path")
        # 请求路径
        self.__path = self.__get_correct_path(Utils.extract_attrs_from_dict(interface_info, "path", "$value"),
                                              self.__desc)
        xmlTrack.pop()
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "header"), "header")
        # 请求头
        self.__header = self.__get_correct_header(Utils.extract_attrs_from_dict(interface_info, "header", "$value"))
        xmlTrack.pop()
        # 得到正确的请求
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "param"), "param")
        self.__param = self.__get_correct_param(Utils.extract_attrs_from_dict(interface_info, "param", "$value"))
        xmlTrack.pop()
        # 得到正确的请求体和请求体格式
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "body"), "body")
        self.__body, self.__body_type = self.__get_correct_body_and_body_type(
            Utils.extract_attrs_from_dict(interface_info, "body", "$value"),
            Utils.extract_attrs_from_dict(interface_info, "body", "type"))
        xmlTrack.pop()
        # 请求端口
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "port"), "port")
        self.__port = self.__get_correct_port(Utils.extract_attrs_from_dict(interface_info, "port", "$value"))
        xmlTrack.pop()
        # 请求服务器
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "server"), "server")
        self.__server = self.__get_correct_server(Utils.extract_attrs_from_dict(interface_info, "server", "$value"))
        xmlTrack.pop()
        # http类型传递文件
        # {name:(path,imei)}
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "files"), "files")
        self.__files = self.__get_correct_files(Utils.extract_attrs_from_dict(interface_info, "files", "file"))
        xmlTrack.pop()
        # cookies
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "cookies"), "cookies")
        self.__cookies = self.__get_correct_cookies(Utils.extract_attrs_from_dict(interface_info, "cookies", "$value"))
        xmlTrack.pop()
        # auth
        xmlTrack.push_source_data(Utils.extract_attrs_from_dict(interface_info, "auth"), "auth")
        self.__auth = self.__get_correct_auth(Utils.extract_attrs_from_dict(interface_info, "auth", "$value"))
        # auth type
        self.__auth_type = self.__get_correct_auth_type(Utils.extract_attrs_from_dict(interface_info, "auth", "type"))
        xmlTrack.pop()
        xmlTrack.pop()

    def __getitem__(self, item):
        return getattr(self, item)

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def desc(self):
        return self.__desc

    @desc.setter
    def desc(self, desc):
        self.__desc = desc

    @property
    def protocol(self):
        return self.__protocol

    @protocol.setter
    def protocol(self, protocol):
        self.__protocol = protocol

    @property
    def path(self):
        return self.__path

    @path.setter
    def path(self, path):
        self.__path = path

    @property
    def header(self):
        return self.__header

    @header.setter
    def header(self, header: Union[str, None]):
        """
        设置header
        :param header:
        :return:
        """
        if type(header) != str and header is not None:
            raise MyException("必须是字符串!而不是{}".format(type(header)))
        self.__header = header

    @property
    def param(self):
        """
        返回param
        :return:
        """
        return self.__param

    @param.setter
    def param(self, param):
        self.__param = param

    @property
    def body(self):
        """
        返回body
        :return:
        """
        return self.__body

    @body.setter
    def body(self, body: Union[str, None]):
        """
        设置body
        :param body:
        :return:
        """
        if type(body) != str and body is not None:
            raise MyException("必须是字符串!而不是{}".format(type(body)))
        self.__body = body

    @property
    def body_type(self):
        return self.__body_type

    @body_type.setter
    def body_type(self, body_type):
        self.__body_type = body_type

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, port):
        self.__port = port

    @property
    def server(self):
        return self.__server

    @server.setter
    def server(self, server):
        self.__server = server

    @property
    def method(self):
        return self.__method

    @method.setter
    def method(self, method):
        self.__method = method

    @property
    def files(self):
        return self.__files

    @files.setter
    def files(self, files):
        self.__files = files

    @property
    def cookies(self):
        return self.__cookies

    @cookies.setter
    def cookies(self, cookies):
        self.__cookies = cookies

    @property
    def auth(self):
        return self.__auth

    @auth.setter
    def auth(self, auth):
        self.__auth = auth

    @property
    def auth_type(self):
        return self.__auth_type

    @auth_type.setter
    def auth_type(self, auth_type):
        self.__auth_type = auth_type

    @staticmethod
    def __get_correct_auth_type(auth_type):
        """
        得到争取的auth_type
        :param auth_type:
        :return:
        """
        # 如果auth_type是空，直接原样返回
        if auth_type is None or auth_type == "":
            return None
        try:
            header = Express.calculate_str(auth_type)
        except Exception as e:
            raise MyException("解析auth时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    @staticmethod
    def __get_correct_auth(auth):
        """
        得到正确的auth
        :param auth:
        :return:
        """
        # 如果auth是空，直接原样返回
        if auth is None or auth == "":
            return None
        try:
            header = Express.calculate_str(auth)
        except Exception as e:
            raise MyException("解析auth时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    @staticmethod
    def __get_correct_cookies(cookies):
        """
        得到正确的cookies字符串
        :param cookies:
        :return:
        """
        # 如果cookies是空，直接原样返回
        if cookies is None or cookies == "":
            return None
        try:
            header = Express.calculate_str(cookies)
        except Exception as e:
            raise MyException("解析cookies时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    @staticmethod
    def __get_correct_path(path, desc):
        """
        得到正确的路径
        :param path:
        :return:
        """
        if path is None:
            return path
        if path and path.startswith("/"):
            path = path[1:]
        try:
            path = Express.calculate_str(path)
        except Exception as e:
            raise MyException("解析path时产生了一个错误，具体的错误内容如下：{}".format(e))
        return path

    @staticmethod
    def __get_correct_header(header):
        """
        根据协议取到正确的请求头
        :param header:
        :return:
        """
        # 如果请求头是空，直接原样返回
        if header is None or header == "":
            return header
        try:
            header = Express.calculate_str(header)
        except Exception as e:
            raise MyException("解析header时产生了一个错误，具体的错误内容如下：{}".format(e))
        return header

    @staticmethod
    def __get_correct_protocol(protocol):
        """
        得到正确的协议，协议应全是小写
        :param protocol:
        :return:
        """
        if not protocol:
            raise MyException("此接口的协议为空！")
        protocol = protocol.lower()
        if protocol in ["http", "tcp", "https", "sql"]:
            return protocol
        raise MyException("此接口还不支持[{}]协议!".format(protocol))

    @staticmethod
    def __get_correct_desc(desc):
        """
        获得正确的描述，描述不能为空
        :param desc:
        :return:
        """
        if not desc:
            raise MyException("此接口的描述为空！}")
        return desc

    @staticmethod
    def __get_correct_name(name):
        """
        获得正确的name，name不能为空
        :param name:
        :return:
        """
        if not name:
            raise MyException("接口的名称不能为空!")
        return name

    @staticmethod
    def __get_correct_param(param):
        if param is None:
            return None
        return Express.calculate_str(param)

    @staticmethod
    def __get_correct_body_and_body_type(body, body_type):
        """
        得到正确的请求体和请求体格式
        :param body:
        :param body_type:
        :return:
        """
        # 先判断请求体和请求体格式是否为空
        if body is None and body_type is None:
            return None, None
        # 当请求体不为空，请求体格式为空时，默认请求体格式为"key_value"
        if body_type:
            body_type = body_type.lower()
        if body and body_type is None:
            body_type = "key_value"
        try:
            body = Express.calculate_str(body)
        except Exception as e:
            raise MyException("解析body时产生了一个错误，具体的错误内容如下：{}".format(e))
        return body, body_type

    @staticmethod
    def __get_correct_port(port):
        """
        得到正确的端口
        :param port:
        :return:
        """
        # 如果端口是空，直接原样返回
        if port is None or port == "":
            return port
        try:
            port = Express.calculate_str(port)
        except Exception as e:
            raise MyException("解析port时产生了一个错误，具体的错误内容如下：{}".format(e))
        return port

    @staticmethod
    def __get_correct_server(server):
        """
        得到正确的服务器
        :param server:
        :return:
        """
        if server is None or server == "":
            return server
        try:
            server = Express.calculate_str(server)
        except Exception as e:
            raise MyException("解析server时产生了一个错误，具体的错误内容如下：{}".format(e))
        return server

    @staticmethod
    def __get_correct_method(method, protocol):
        """
        得到正确的http请求方法
        :param method:
        :param protocol:
        :return:
        """
        if method:
            method = method.lower()
        if protocol in ["http", "https"] and method not in ["post", "get", "delete", "patch", "put"]:
            raise MyException("此接口配置有误，HTTP接口的请求方法不能是[{}],只能是GET,POST,DELETE,PATCH,PUT!".format(method))
        return method

    @staticmethod
    def __check_need_to_be_replaced(param):
        """
        检查变量需要被替换吗？
        :param param:
        :return:
        """
        if type(param) == dict and len(param) == 0:
            return True
        return False

    def __get_correct_files(self, files):
        """
        取得正确的files
        :param files:
        :return:
        """
        if files is None:
            return None
        if files == "":
            return None
        files = files if type(files) == list else [files]
        n_files = {}
        for file in files:
            xmlTrack.push_source_data(file, "file")
            file_name = file.get("$value")
            mime = file.get("mime")
            if mime == "":
                mime = None
            name = file.get("name")
            if name is None or name == "":
                raise MyException("文件的name不能为空！")
            n_files[name] = (file_name, mime)
            xmlTrack.pop()
        if n_files == {}:
            return None
        self.__body_type = "key_value"
        return n_files


class InterfaceDict(object):
    def __init__(self):
        """
        读取所有的接口信息
        :return: None
        """
        # 接口信息存储字典
        self.__interface_dict = dict()

    def get(self, interface_name) -> Interface:
        """
        取得接口
        :return:
        """
        if config.env_flag:
            config.env_flag = False
            self.__interface_dict.clear()
        if self.__interface_dict.get(interface_name) is None:
            self.__interface_dict[interface_name] = Interface(interface_name)
        return self.__interface_dict.get(interface_name)
