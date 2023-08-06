# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
from .beautify_json import BeautifyJson
from .beautify_xml import BeautifyXml


class Beautify(object):
    def __init__(self, data, _type):
        """
        美化输出
        :param data: 数据
        :param _type: 类型
        """
        self.__data = data
        self.__type = _type

    def beautify(self):
        """
        返回美化后的结果
        :return:
        """
        if self.__type in ["json","key_value","form_gb18030"] and self.__data is not None:
            return "\n{}".format(BeautifyJson(self.__data).beautify())
        if self.__type in ["xml"] and self.__data is not None:
            return "{}".format(BeautifyXml(self.__data).beautify())
        return self.__data
