# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: frame config class
"""
import configparser
import os
import sys
import puppy
from ..express.express import Express

from ..utils.utils import Utils
from ...exception.my_exception import MyException


class ConfigLoader(object):
    """
    项目的配置加载器，将一次性读取所有的配置
    """

    def __init__(self):
        # 取到项目根目录
        self.__base_path = ConfigLoader.get_base_path()
        # puppy框架目录
        self.__puppy_path = puppy.__path__[0]
        # 用来存储读取的原始配置
        self.__config = {
            "cases_path": os.path.join(self.__base_path, 'test_case'),
            "test_data_path": os.path.join(self.__base_path, 'test_data'),
            "flow_path": os.path.join(self.__base_path, 'flow'),
            "report_path": os.path.join(self.__base_path, "report"),
            "api_file_path": os.path.join(self.__base_path, "interface"),
            "jar_file_path": os.path.join(self.__base_path, "file/jar"),
            "js_file_path": os.path.join(self.__base_path, "file/js"),
            "file_path": os.path.join(self.__base_path, "file"),
            "inner_function_file": os.path.join(self.__puppy_path, "core", "function", "express", "function.py"),
            "outer_function_file": os.path.join(self.__base_path, "file/func.py"),
            "package_for_selenium": os.path.join(self.__base_path, "seleniums"),
            "browser": "Chrome",
            "driver": "None",
            "base_path": self.__base_path,
            "project_path": self.__base_path,
            "puppy_path": self.__puppy_path,
            "format_str_length": "-1",
            "report_name": "API自动化测试报告",
            "debug": "false",
            "cases": "test*.py",
            "http_connection_timeout": "50",
            "http_read_timeout": "50",
            "tcp_timeout": "60",
            "max_number_non_select_sql": "10",
            "resource_thread_sleep_time": "1",
            "progress_thread_sleep_time": "1",
            "action_case": "None",
            "db_keep_connection_time": "30",
            "testing": "false",
            "single_testing": "true",
            "the_global_inspection": "false",
            "the_global_inspection_type": "auto",
            "beautify": "true",
            "fold_text": "false",
            "fold_text_when_more_than_lines": "5",
            "debug_format": "{year}-{month}-{day} {hour}:{minute}:{second}.{microsecond} {filename} - <{tag}> <{line}>: {msg}",
            "env": "config",
            "db_info": None
        }
        # 用来存储读取的原始变量
        self.__vars = dict()
        # 读取和计算文件内的配置及变量
        self.__load_config_from_file()
        # 记录env是否切换
        self.__env_flag = True
        # 记录当前环境
        self.__env = "config"

    def __load_config_from_file(self):
        """
        用来载入文件内的配置和变量
        """
        config_file = "{}/file/conf/config.cfg".format(self.__base_path)
        if not os.path.exists(config_file):
            return
        # 构造一个配置对象
        conf_loader = configparser.ConfigParser()
        # 读取文件里的配置和变量
        if config_file:
            conf_loader.read(config_file, encoding='utf-8')
        sections = conf_loader.sections()
        for section in sections:
            options = conf_loader.options(section)
            section_dict = dict()
            for option in options:
                if section == "config" and option in self.__config.keys():
                    self.__config[option] = Express.calculate_in_config(conf_loader.get(section, option), self.__config)
                else:
                    section_dict[option] = Express.calculate_in_config(conf_loader.get(section, option), section_dict)
            self.__vars[section] = section_dict

    @staticmethod
    def get_base_path():
        path = sys.path[0]
        if path.endswith("test_case"):
            return os.path.dirname(path)
        return path

    @staticmethod
    def __process_config(name, cfg, _type):
        """处理配置"""
        if type(cfg) is not _type:
            if _type is bool:
                if cfg in ["True", "1", "true"]:
                    return True
                elif cfg in ["False", "0", "false"]:
                    return False
                else:
                    raise MyException(" {} 配置项配置不正确，只能是True或False，不能是 {}".format(name, cfg))
            elif _type is int:
                if Utils.is_number(cfg):
                    return int(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
            elif _type is float:
                if Utils.is_float(cfg):
                    return float(cfg)
                else:
                    raise MyException(" {} 配置项不正确，只能是数字，不能是 {}".format(name, cfg))
        return cfg

    def get_config(self, name, _type=str):
        """
        得到配置项，返回_type指定类型
        :param _type:
        :param name:
        :return: 如果配置不存在则返回None
        """
        if name not in self.__config.keys():
            raise MyException("配置不存在：{}".format(name))
        return self.__process_config(name, self.__config.get(name), _type)

    def have_config(self, name):
        """
        判断是否存在配置
        :param name:
        :return:
        """
        try:
            self.get_config(name)
            return True
        except:
            return False

    def set_config(self, name, value):
        """
        设置配置项，该配置项不会被写入文件。
        :param name:
        :param value:
        :return:
        """
        self.__config[name] = value

    def all_cases(self):
        self.set_config("cases", "test*.py")

    def start_test(self):
        print("自动化脚本测试开始！")
        self.set_config("fold_text", False)
        self.set_config("format_str_length", -1)
        self.set_config("testing", True)
        self.set_config("single_testing", False)
        self.set_config("debug", False)
        self.set_config("the_global_inspection", True)

    def end_test(self):
        print("自动化脚本测试结束！")
        self.set_config("testing", False)

    def test(self, case):
        self.set_config("action_case", case)
        self.env = self.get_config("env")

    @property
    def env(self):
        return self.__env

    @property
    def env_flag(self):
        return self.__env_flag

    @env_flag.setter
    def env_flag(self, flag):
        self.__env_flag = flag

    @env.setter
    def env(self, env):
        if env not in self.__vars.keys():
            raise MyException("{} 环境不存在".format(env))
        if self.env == env:
            return
        self.__env_flag = True
        self.__env = env

    @property
    def report_name(self):
        return self.get_config("report_name")

    @property
    def cases(self):
        cases = self.get_config("cases")
        cases_list = cases.split("|")
        return cases_list

    @property
    def configs(self):
        return self.__config

    @property
    def vars(self):
        '''
        返回当前环境变量指定的变量组
        '''
        return self.__vars.get(self.env)


config = ConfigLoader()
