# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: http client
"""
import os
from io import BufferedReader
import requests
from requests import Session
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from requests.cookies import RequestsCookieJar
from .client import AbstractClient
from ....data.interface import Interface
from ....exception.client import HttpMethodIsNotSupportedException
from ....exception.my_exception import MyException
from ....exception.other import FileIsNotExistsException
from ....function.cfg.config import config
from ....function.parse.json_parse import JsonParse
from ....function.utils.utils import Utils
from ....printer.format_printer import Printer


class HTTP(AbstractClient):
    """
    HTTP 接口客户端
    """

    def __init__(self, interface_info: Interface, interface_data: dict, context: dict, session=None):
        """
        HTTP 接口客户端
        :param interface_info:接口信息
        :param interface_data: 接口数据
        :param context: 场景上下文
        :return:
        """
        # 场景上下文
        super().__init__(interface_info, interface_data, context)
        # requests客户端
        self.__session = session
        if not session:
            self.__session = requests.session()

    def __get_method(self):
        method = self._interface_info.method
        if method not in ["post", "get", "patch", "put", "delete"]:
            raise HttpMethodIsNotSupportedException(method)
        return method

    def __get_header(self):
        """
        准备header
        :return:
        """
        if self._interface_info.header is not None and not JsonParse.is_correct_json(self._interface_info.header):
            raise MyException("调用的接口请求头：{}格式不正确，请检查！".format(self._interface_info.header))
        return JsonParse.to_json(self._interface_info.header)

    def __get_url(self):
        """
        准备url
        :return:
        """
        path = self._interface_info.path
        port = self._interface_info.port
        server = self._interface_info.server
        protocol = self._interface_info.protocol
        # 构造一个url
        return self.__structure_url(protocol, server, port, path)

    def __get_body(self):
        """
        获得body
        :return:
        """
        body_type = self._interface_info.body_type
        body = self._interface_info.body
        param = self._interface_info.param
        method = self._interface_info.method
        if body is not None:
            if body_type == "key_value":
                if not JsonParse.is_correct_json_dict(body):
                    raise MyException("请求报文不是正确的表单格式，请检查！该报文为:\n{}".format(body))
                return JsonParse.to_json(body)
            elif body_type in ["xml"]:
                return body.encode("utf-8").decode("ltatin1")
            elif body_type == "json":
                if not JsonParse.is_correct_json(body):
                    raise MyException("请求报文不是正确的json报文，请检查！该报文为:\n{}".format(body))
                return JsonParse.to_json_str(JsonParse.to_json(body))
            elif body_type == "form_gb18030":
                if not JsonParse.is_correct_json_dict(body):
                    raise MyException("请求报文不是正确的表单格式，请检查！该报文为:\n{}".format(body))
                return Utils.quote_(JsonParse.to_json(body), "gb18030")
            elif body_type == "string":
                return body
            else:
                raise MyException("HTTP的 {} 请求不支持对此种格式 {} 的处理".format(method, body_type))
        if param is not None and method == "get":
            if not JsonParse.is_correct_json_dict(param):
                raise MyException("请求参数不是正确的键值对格式，请检查！该参数为:\n{}".format(param))
            return JsonParse.to_json(param)

    def __get_param(self):
        """
        获得param
        :return:
        """
        param = self._interface_info.param
        # 对参数处理
        if param is not None:
            if not JsonParse.is_correct_json_dict(param):
                raise MyException("请求参数不是正确的键值对格式，请检查！")
            param = JsonParse.to_json(param)
        return param

    def __get_files(self):
        """
        处理文件
        :return:
        """
        files = self._interface_info.files
        method = self._interface_info.method
        if files is None:
            return None
        if len(files) == 0:
            return None
        if method != "post":
            raise MyException("包含文件的HTTP请求必须使用post方式！")
        n_files = {}
        for name, other in files.items():
            file = other[0]
            if not file.startswith("/"):
                # 需要拼接根目录
                file = os.path.join(config.get_config("base_path"), file)
            # 判断文件是否存在
            if not os.path.exists(file):
                raise FileIsNotExistsException(file)
            mime = other[1]
            n_files[name] = (os.path.basename(file), open(file, 'rb'), mime)
        return n_files

    def __get_cookies(self):
        """
        取得cookie对象
        :return:
        """
        # 先判断cookies是否存在
        cookies = self._interface_info.cookies
        if cookies is None:
            return None
        # 再判断cookies是否是正确的格式
        if not JsonParse.is_correct_json_dict(cookies):
            raise MyException("不是正确格式的cookies")
        cookie_object = RequestsCookieJar()
        cookies_dict = JsonParse.loads(cookies)
        for cookie_name, cookie_value in cookies_dict.items():
            if type(cookie_value) is dict:
                v = cookie_value.get("value")
                # 移除value
                cookie_value.pop("value")
                # 附加其他参数
                cookie_object.set(cookie_name, v, **cookie_value)
            else:
                cookie_object.set(cookie_name, cookie_value)
        return cookie_object

    def __get_auth(self):
        # 先判断cookies是否存在
        auth = self._interface_info.auth
        auth_type = self._interface_info.auth_type
        if auth is None:
            return None
        # 再判断cookies是否是正确的格式
        if not JsonParse.is_correct_json_dict(auth):
            raise MyException("不是正确格式的认证")
        auth = JsonParse.loads(auth)
        # 返回对应的认证对象
        if auth_type in [None, "HTTPBasicAuth"]:
            return HTTPBasicAuth(**auth)
        elif auth_type == "HTTPDigestAuth":
            return HTTPDigestAuth(**auth)
        else:
            raise MyException("该认证方式 {} 暂不支持".format(auth_type))

    def __print_req(self, url, files):
        """
        打印请求
        :return:
        """
        body_type = self._interface_info.body_type
        method = self._interface_info.method
        body = self._interface_info.body
        param = self._interface_info.param
        header = self._interface_info.header
        cookies = self._interface_info.cookies
        auth = self._interface_info.auth
        desc = self._interface_info.desc
        if method == "get":
            if body is not None:
                Printer.print_request_info("GET", desc, url, header, body, body_type, cookies=cookies, auth=auth)
                return
            if param is not None:
                Printer.print_request_info("GET", desc, url, header, param, "key_value", cookies=cookies, auth=auth)
                return
            Printer.print_request_info("GET", desc, url, header, None, None, cookies=cookies, auth=auth)
        else:
            # 打印关键信息
            Printer.print_request_info(method.upper(), desc, url, header, body, body_type, files, param, cookies, auth)

    def _request(self):
        """
        发送请求前
        :return:
        """
        method = self.__get_method()
        header = self.__get_header()
        url = self.__get_url()
        files = self.__get_files()
        body = self.__get_body()
        param = self.__get_param()
        cookies = self.__get_cookies()
        auth = self.__get_auth()
        self.__print_req(url, files)
        # 发出请求并获得结果
        self.__send_request(method, url, param, body, header, files, cookies, auth)
        # 打印响应结果
        Printer.print_response_info(method.upper(), self._res)

    def __send_request(self, method, url, param, body, headers, files=None, cookies=None, auth=None):
        """
        发出一个指定方法的请求，并处理结果，将返回响应状态，响应正文，响应头
        :param method:
        :param url:
        :param body:
        :param headers:
        :return:
        """
        # 记录错误信息
        # 1代表requests.exceptions.ConnectionError这个错误
        err_type = -1
        try:
            if files:
                r = self.__session.post(url, data=body, headers=headers, files=files, cookies=cookies, auth=auth)
            else:
                if method == "get":
                    r = self.__session.get(url, params=body, headers=headers, cookies=cookies, auth=auth, timeout=(
                        config.get_config("http_connection_timeout", float),
                        config.get_config("http_read_timeout", float)))
                elif method == "patch":
                    r = self.__session.patch(url, params=param, data=body, headers=headers, cookies=cookies, auth=auth,
                                             timeout=(
                                                 config.get_config("http_connection_timeout", float),
                                                 config.get_config("http_read_timeout", float)))
                elif method == "put":
                    r = self.__session.put(url, params=param, data=body, headers=headers, cookies=cookies, auth=auth,
                                           timeout=(config.get_config("http_connection_timeout", float),
                                                    config.get_config("http_read_timeout", float)))
                elif method == "delete":
                    r = self.__session.delete(url, params=param, data=body, headers=headers, cookies=cookies, auth=auth,
                                              timeout=(config.get_config("http_connection_timeout", float),
                                                       config.get_config("http_read_timeout", float)))
                else:
                    r = self.__session.post(url, params=param, data=body, headers=headers, cookies=cookies, auth=auth,
                                            timeout=(config.get_config("http_connection_timeout", float),
                                                     config.get_config("http_read_timeout", float)))
            # 设置响应的值
            self._res.code = r.status_code
            self._res.text = str(r.text).strip()
            self._res.header = dict(r.headers)
            self._res.header_type = "dict"
        except requests.exceptions.ConnectionError:
            err_type = 1
        except requests.exceptions.ReadTimeout:
            err_type = 2
        except Exception as e:
            raise e
        finally:
            if type(files) is dict:
                for n, f in files.items():
                    if type(f[1]) is BufferedReader:
                        f[1].close()
            if err_type == 1:
                raise MyException("计算机拒绝了您的连接，请检查请求地址是否正确、网络是否正常!")
            elif err_type == 2:
                raise MyException("读取响应超时，请检查服务器是否正常！")

    @staticmethod
    def __structure_url(protocol, server, port, path):
        """
        构造链接
        :param protocol:
        :param server:
        :param port:
        :param path:
        :return:
        """
        url = ""
        if port:
            url += "{}://{}:{}/".format(protocol, server, port)
        else:
            url += "{}://{}/".format(protocol, server)
        if path:
            url += path
        return url

    @property
    def session(self) -> Session:
        """
        返回Session对象
        :return:
        """
        return self.__session
