"""
    author: Li Junxian
    function:is used to process function
"""
import importlib
import os
import re


def demo():
    pass


class Module(object):
    """
    功能读取、调用、帮助信息输出
    """
    def __init__(self, module_file):
        """
        模块的文件:模块文件全路径
        """
        self.__module_file = module_file
        if not os.path.exists(module_file):
            raise Exception("{} 不存在".format(module_file))
        self.__func = list()
        self.__class = list()
        self.__var = list()
        self.__m=list()
        self.__module=None
        self.__get_module()

    def __get_module(self):
        """
        取得func信息
        """
        self.__module = importlib.import_module(self.__get_module_name())
        for name in dir(self.__module):
            if name in ["builtins"]:
                continue
            if name.startswith("__"):
                continue
            o = getattr(self.__module, name)
            if type(o) is type:
                self.__class.append(name)
            elif type(o) is type(demo):
                self.__func.append(name)
            elif type(o) is type(os):
                self.__m.append(name)
            else:
                self.__var.append(name)

    def __get_module_name(self):
        """
        获取到包名和模块名
        """
        # 取得根目录
        from ..cfg.config import config
        base_path = config.get_config("base_path")
        # 取得puppy模块的目录
        puppy_path = os.path.dirname(config.get_config("puppy_path"))
        # 将文件名拆开
        model_name, suffix = os.path.splitext(self.__module_file)
        if puppy_path in model_name:
            model_name = model_name.replace(puppy_path, "")
        if base_path in model_name:
            model_name = model_name.replace(base_path, "")
        if model_name[0] in ["\\", "/"]:
            model_name = model_name[1:]
        # 遍历字符串
        new_model_name = ""
        for s in list(model_name):
            if s in ["/", "\\"]:
                new_model_name += "."
            else:
                new_model_name += s
        return new_model_name

    def has_var(self, name):
        """
        判断是否有此变量
        :param name:
        :return:
        """
        if name in self.__var:
            return True
        return False

    def has_func(self, name):
        """
        判断是否有此函数
        :param name:
        :return:
        """
        if name in self.__func:
            return True
        return False

    def has_class(self, name):
        """
        判断是否由此类
        :param name:
        :return:
        """
        if name in self.__class:
            return True
        return False

    def has_module(self, name):
        """
        判断是否由此模块
        :param name:
        :return:
        """
        if name in self.__m:
            return True
        return False

    def var(self, name):
        """
        取得要调用的类
        :param name:
        :return:
        """
        if not self.has_var(name):
            raise Exception("此 {} 变量不存在!".format(name))
        return getattr(self.__module,name)

    def clazz(self, name):
        """
        取得要调用的类
        :param name:
        :return:
        """
        if not self.has_class(name):
            raise Exception("此 {} 类不存在!".format(name))
        return getattr(self.__module,name)

    def func(self, name):
        """
        取得要调用的方法
        """
        if not self.has_func(name):
            raise Exception("此 {} 函数不存在!".format(name))
        return getattr(self.__module,name)

    def module(self,name):
        """
        取得要调用的模块
        :param name:
        :return:
        """
        if not self.has_module(name):
            raise Exception("此 {} 模块不存在!".format(name))
        return getattr(self.__module, name)

outer_module = None
inner_module = None


def outer() -> Module:
    global outer_module
    if outer_module is None:
        from ..cfg.config import config
        outer_module = Module(config.get_config("outer_function_file"))
    return outer_module


def inner() -> Module:
    global inner_module
    if inner_module is None:
        from ..cfg.config import config
        inner_module = Module(config.get_config("inner_function_file"))
    return inner_module
