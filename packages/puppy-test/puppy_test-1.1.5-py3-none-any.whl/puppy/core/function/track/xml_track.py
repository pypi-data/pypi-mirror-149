import os

from puppy.core.function.utils.utils import Utils


class XMLTrack(object):
    def __init__(self):
        self.__list = list()

    def pop(self):
        self.__list.pop()

    def push(self, file_path, row, tag):
        self.__list.append({"file_path": file_path, "row": row, "tag": tag})

    def push_sorted_data(self, data: dict):
        """
        推入排序后的数据
        :param data:
        :return:
        """
        tag = data.get("name")
        file_path = Utils.extract_attrs_from_dict(data, "value", "$file_path")
        if file_path is None:
            file_path = "Unknown File"
        row = Utils.extract_attrs_from_dict(data, "value", "$row")
        if row is None:
            file_path = "Unknown Row"
        self.__list.append({"file_path": file_path, "row": row, "tag": tag})

    def push_source_data(self, data: dict, tag):
        """
        推入原始数据
        :param data:
        :param tag:
        :return:
        """
        file_path, row = Utils.extract_path_and_row(data)
        self.__list.append({"file_path": file_path, "row": row, "tag": tag})

    def __get_last(self):
        if len(self.__list) <= 0:
            return None
        return self.__list[len(self.__list) - 1]

    def current_path_row(self):
        last = self.__get_last()
        if last is None:
            return "Unknown File", "Unknown Row"
        return last.get("file_path"), last.get("row")

    def current_tag(self):
        last = self.__get_last()
        if last is None:
            return "Unknown Tag"
        return last.get("tag")

    def current_row(self):
        last = self.__get_last()
        if last is None:
            return "Unknown Row"
        return last.get("row")

    def current_file_path(self):
        last = self.__get_last()
        if last is None:
            return "Unknown File Path"
        return last.get("file_path")

    def current_file_name(self):
        last = self.__get_last()
        if last is None:
            return "Unknown File Name"
        file_path = last.get("file_path")
        file_name = os.path.split(file_path)[1]
        return file_name


xmlTrack = XMLTrack()
xmlTrack.push("C:\\a\\a.txt", 12, "ss")
