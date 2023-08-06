# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: tcp client
"""
import socket
from .client import AbstractClient
from ....data.interface import Interface
from ....exception.my_exception import MyException
from ....function.cfg.config import config
from ....printer.format_printer import Printer


class TCP(AbstractClient):
    """
    TCP 接口客户端
    """

    def __init__(self, interface_info: Interface, interface_data: dict, context: dict):
        """
        HTTP 接口客户端
        :param interface_info:接口信息
        :param interface_data: 接口数据
        :param context: 场景上下文
        :return:
        """
        super().__init__(interface_info, interface_data, context)

    def _request(self):
        # 获得请求体
        body = self._interface_info.body
        body = "" if body is None else body
        h = self._interface_info.header
        h = "" if h is None else h
        data = "{}{}".format(h, body)
        data = data
        # 构造请求头
        header = self.__get_header(8, len(data.encode()))
        # 构造url
        port = self._interface_info.port
        server = self._interface_info.server
        Printer.print_request_info("TCP", self._interface_info.desc, "{}:{}".format(server, port), header, data,
                                   self._interface_info.body_type)
        client = TcpClient()
        res = client.request(server, port, header, data)
        self._res.code = res.code
        self._res.header = res.header
        self._res.text = res.text
        # 打印响应结果
        Printer.print_response_info("TCP", self._res)

    @staticmethod
    def __get_header(header_len, body_len):
        # 根据header（定长8）和body的长度，生成请求报文的header
        # sb的值 ，i在3 - 8之间，补5个0，再加上body总长度
        sb = ''
        head = str(body_len)
        for i in range(len(head), header_len):
            sb += '0'
        sb += str(body_len)
        return sb


class TcpClient(object):
    def __init__(self):
        self.__timeout = config.get_config("tcp_timeout",float)
        self.__encoding = "utf-8"

    def request(self, server, port, header: str, data: str):
        s = None
        try:
            # 检查端口
            self.__check_port(port)
            # 创建TCP套接字
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 设置超时时间
            s.settimeout(self.__timeout)
            # 连接到端口
            s.connect((server, int(port)))
            # 对数据编码
            data = data.encode(self.__encoding)
            # 对头编码
            header = header.encode(self.__encoding)
            # 发送头
            s.sendall(header)
            # 发送数据
            s.sendall(data)
            # 再次设置超时时间
            s.settimeout(self.__timeout)
            # 先接收8位头部
            res_h = s.recv(8)
            if res_h is None or res_h == "" or res_h==b'':
                raise MyException("接收的响应头为空，请检查请求报文是否正确")
            # 获得接下来的数据宽度
            width = int(res_h)
            # 定义完成的数据byte
            res_data_of_byte = bytes()
            # 当接收的数据小于0时
            while width > 0:
                # 再次设置超时时间
                s.settimeout(self.__timeout)
                # 每次接收1024个字节
                byte_data = s.recv(1024)
                # 减去实际接收的数据宽度
                width = width - len(byte_data)
                # 拼接返回的数据
                res_data_of_byte += byte_data
            return TcpRes(200, res_h.decode(self.__encoding), res_data_of_byte.decode(self.__encoding))
        except Exception:
            raise
        except ConnectionRefusedError:
            raise MyException("[WinError 10061] 由于目标计算机拒绝，无法连接。")
        finally:
            if s:
                s.close()

    @staticmethod
    def __check_port(port):
        if not port.isnumeric():
            raise MyException("TCP接口的端口必须是数字，不能是：{}".format(port))


class TcpRes(object):
    def __init__(self, code, header, text):
        self.__code = code
        self.__header = header
        self.__text = text

    @property
    def code(self):
        return self.__code

    @property
    def header(self):
        return self.__header

    @property
    def text(self):
        return self.__text
