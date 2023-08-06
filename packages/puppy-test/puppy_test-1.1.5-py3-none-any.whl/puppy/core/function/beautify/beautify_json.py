# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: beautify json
"""
import json
import re
from ..parse.json_parse import JsonParse
from ..utils.utils import Utils
from ...exception.my_exception import MyException


class BeautifyJson(object):
    __blank_re = re.compile(r"\s")
    __blank = Utils.BLANK_CHAR
    __single = 4

    def __init__(self, json: str):
        """
        待美化的json字符串
        :param json:
        """
        self.__json = json
        if not JsonParse.is_correct_json(json):
            raise MyException("{}不是正确的json字符串".format(json))

    def beautify(self):
        """
        采用周老师的写法
        :return:
        """
        number_of_blank = 4
        prefix = str(self.__blank * self.__single)
        indent_text = self.__blank * number_of_blank
        json_o = JsonParse.to_json(self.__json)
        res = prefix + json.dumps(json_o, sort_keys=False, ensure_ascii=False, indent=indent_text).replace('\n','\n' + indent_text)
        return res

    #
    # def beautify(self):
    #     """
    #     获得美化后的json字符串
    #     :return:
    #     """
    #     # 空白字符
    #     # 空白字符所有数量
    #     number_of_blank = 3
    #     # 单级空白字符数量
    #     json_list = list(self.__json)
    #     double_quotation_marks = False
    #     backslash = False
    #     first = True
    #     last_letter = None
    #     for letter in json_list:
    #         if BeautifyJson.__blank_re.fullmatch(letter) and not double_quotation_marks:
    #             pass
    #         elif letter == "\\":
    #             backslash = not backslash
    #             self.__beautified_json += letter
    #         elif letter == '"' and not backslash:
    #             double_quotation_marks = not double_quotation_marks
    #             self.__beautified_json += '"'
    #         elif letter in ['{', '['] and not double_quotation_marks:
    #             if first:
    #                 self.__beautified_json += "{}{}\n".format(BeautifyJson.__blank * number_of_blank, letter)
    #                 first = False
    #             else:
    #                 self.__beautified_json += "{}\n".format(letter)
    #             number_of_blank += BeautifyJson.__single
    #             self.__beautified_json += BeautifyJson.__blank * number_of_blank
    #         elif letter == ':' and not double_quotation_marks:
    #             self.__beautified_json += ": "
    #         elif letter in [']', '}'] and not double_quotation_marks:
    #             number_of_blank -= BeautifyJson.__single
    #             if last_letter in ['[', '{']:
    #                 self.__beautified_json=self.__beautified_json.rstrip()
    #                 self.__beautified_json += "{}".format(letter)
    #             else:
    #                 self.__beautified_json += "\n{}{}".format(BeautifyJson.__blank * number_of_blank, letter)
    #         elif letter == ',' and not double_quotation_marks:
    #             self.__beautified_json += ",\n{}".format(BeautifyJson.__blank * number_of_blank)
    #         else:
    #             backslash = False
    #             self.__beautified_json += letter
    #         last_letter = letter
    #     return self.__beautified_json
