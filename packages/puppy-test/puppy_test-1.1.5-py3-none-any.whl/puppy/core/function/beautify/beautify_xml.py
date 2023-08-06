# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
import re
from ..utils.utils import Utils
from xml.dom.minidom import parseString

class BeautifyXml(object):
    __blank_re = re.compile(r"\s")
    __blank = Utils.BLANK_CHAR
    __single = 4

    def __init__(self, xml: str):
        """
        待美化的json字符串
        :param xml:
        """
        self.__xml = xml


    def beautify(self):
        """
        :return:
        """
        h,b=self.__spilt_xml()
        number_of_blank = 4
        prefix = str(self.__blank * self.__single)
        indent_text = self.__blank * number_of_blank
        xml = parseString(b)
        res="{}{}".format(prefix,xml.toprettyxml(indent=indent_text))
        res=res[:-1].replace('\n', '\n' + indent_text)
        res="{}\n{}".format(h,res)
        return res

    def __spilt_xml(self):
        """提取xml"""
        index=self.__xml.find("<")
        return self.__xml[:index],self.__xml[index:]