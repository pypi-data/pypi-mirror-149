"""
    author: Li Junxian
    function:about java
"""
import importlib.util


if importlib.util.find_spec("jpype") is None:
    raise Exception("要使用jvm，请安装JPype1==1.3.0!")
jpype = importlib.import_module("jpype")


class JVM(object):

    def __new__(cls, *args, **kwargs):
        """
        构造jvm
        :param args:
        :param kwargs:
        """
        if not hasattr(cls, "_dict"):
            setattr(cls, "_dict", dict())
        jvm_dict = getattr(cls, "_dict")
        key = "None"
        if len(args) > 0:
            key = str(args[0])
        if len(kwargs.items()):
            key = str(kwargs.get("jvm_path"))
        if jvm_dict.get(key) is None:
            instance = super().__new__(cls)
            jvm_dict[key] = instance
        return jvm_dict.get(key)

    def __init__(self, jvm_path=None):
        self.__jvm_path = jvm_path
        if not hasattr(self, "__running"):
            jpype.startJVM(jvmpath=self.__jvm_path)
            setattr(self, "__running", True)

    def import_jar(self, jar_path):
        """
        引入jar包到当前jvm环境
        :param jar_path:
        :return:
        """
        jpype.addClassPath(jar_path)

    def JString(self, str):
        """
        取得java String类型的字符串
        :param str:
        :return:
        """
        return jpype.JString(str)

    def JClass(self,class_):
        """
        根据类名引入类
        :param class_:
        :return: 引入类的引用
        """
        return jpype.JClass(class_)

