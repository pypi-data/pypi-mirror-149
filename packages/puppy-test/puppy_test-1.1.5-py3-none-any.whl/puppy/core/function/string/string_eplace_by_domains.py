import re
from types import FunctionType


class StringReplaceByDomains(object):
    def __init__(self, keys_of_domains, domains_checking=None):
        """
        字符串域替换，先使用keys_of_domains从original中找到待替换的列表，再使用domains_checking_param进行检查，如果检查通过，再使用rep进行替换
        :param keys_of_domains: 域的关键值，正则字符串或按顺序的关键值正则字符串
        :param domains_checking_param: 域检查，字符串、字符串组成的列表，函数
        """
        self.__keys_of_domains = keys_of_domains
        self.__domains_checking = domains_checking
        self.__pattern_of_domains = self.__generate_domains_pattern()

    def __generate_domains_pattern(self):
        _type = type(self.__keys_of_domains)
        if _type is str:
            return re.compile(self.__keys_of_domains)
        if _type is list:
            pattern = ""
            for _key in self.__keys_of_domains:
                pattern += r"{}[\s\S]*?".format(_key)
            pattern = pattern[:-8]
            return re.compile(pattern)
        raise Exception("keys_of_domains只能是字符串、数组！")

    def __check_domains(self, string):
        _type = type(self.__domains_checking)
        if _type is None:
            return True
        if _type is str:
            if self.__domains_checking in string:
                return True
            else:
                return False
        if _type is list:
            for _check in self.__domains_checking:
                if _check not in string:
                    return False
            return True
        if _type is FunctionType:
            return self.__domains_checking(string)
        raise Exception("domains_checking只能是字符串、数组、函数！")

    def __rep_string(self, string, rep):
        _type = type(rep)
        if _type is str:
            return rep
        if _type is FunctionType:
            return rep(string)
        raise Exception("rep只能是字符串，函数！")

    def replace(self, original, rep):
        """
        替换
        :param original: 原始串
        :param rep: 字符串，函数
        :return:
        """
        iter = self.__pattern_of_domains.finditer(original)
        results = list()
        for matcher in iter:
            start = matcher.start()
            end = matcher.end()
            source = matcher.group()
            if self.__check_domains(source):
                result = self.__rep_string(source, rep)
                results.append({"start": start, "end": end, "result": result})
        offset = 0
        for _r in results:
            start = _r.get("start") + offset
            end = _r.get("end") + offset
            result = _r.get("result")
            offset += len(result) - (end - start)
            pre = original[:start]
            post = original[end:]
            original = "{}{}{}".format(pre, result, post)
        return original
