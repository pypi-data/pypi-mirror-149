# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function: parse xml file
"""
from xml.sax import make_parser
from xml.sax.handler import ContentHandler, feature_namespaces


class XmlHandler(ContentHandler):
    """
    xml handler
    """

    def __init__(self):
        super().__init__()
        # 当前节点的字典结构
        self.__active_element = None
        # 用来保存当前节点的文本
        self.__active_element_text = ""
        # 用来保存xml结构的栈区
        self.__stack_of_saving_xml_structure = []
        # 用来计算case下的interface、if、while的顺序
        self.__order = 0

    def startElement(self, name, attribute):
        # 遇到一个节点，以节点的名字作为参数,属性值为其字典内容
        if self.__active_element:
            # 如果当前节点不为空，则将当前节点置入栈区
            self.__stack_of_saving_xml_structure.append(self.__active_element)
        # 处理所有属性，对相关的字符进行转义
        at = self.__process_dict(getattr(attribute, "_attrs"))
        # 附上顺序编号
        at["$order"] = self.__order
        self.__order += 1
        # 附上行号
        at["$row"] = self._locator.getLineNumber()
        # 附上文件名
        at["$file_path"] = self._locator.getSystemId()
        # 附上标签名
        # 拼接为字典
        self.__active_element = {name: at}

    def characters(self, content):
        # 如果文字部分是换行、空白、空就直接返回
        if content in ["\n", "", None] or len(content.strip()) == 0:
            return
        text = content.strip()
        if type(self.__active_element) == dict:
            # 提取当前元素的key
            keys = self.__active_element.keys()
            # 针对sql语句的特殊处理
            if "processor" in keys:
                if content.startswith(" "):
                    text = " {}".format(text)
            elif "body" in keys:
                if self.__active_element.get("body").get("name") == "$whole" or self.__active_element.get("body").get(
                        "type") == "sql":
                    if XmlHandler.__is_contains_the_key_of_sql(text) or XmlHandler.__is_contains_the_key_of_sql(
                            self.__active_element_text):
                        if content.startswith(" "):
                            text = " {}".format(text)
        # 拼接文本节点的文字
        self.__active_element_text += text

    def endElement(self, name):
        # 节点的文本内容作为$value值
        active_element = self.__active_element
        active_element_name = self.__active_element.copy().popitem()[0]
        if self.__active_element_text != "":
            active_element_value = self.__active_element[active_element_name]
            active_element_text = self.__active_element_text
            active_element_value['$value'] = self.__process_inputted_string(active_element_text)
            self.__active_element_text = ""
        # 如果堆栈里还有元素，需要处理
        if len(self.__stack_of_saving_xml_structure) <= 0:
            return
        # 从堆栈里弹出最顶上的元素
        pre_element = self.__stack_of_saving_xml_structure.pop()
        pre_element_name = pre_element.copy().popitem()[0]
        # 判断最顶上元素的节点名字对应的值是否为空
        pre_element_value = pre_element[pre_element_name]
        # 再判断对应值是否存在当前元素的名字
        if not pre_element_value.get(active_element_name):
            # 当没有时，将当前元素直接写入
            pre_element_value[active_element_name] = active_element[active_element_name]
        else:
            # 当有时，将其提取出来的值判断是否是数组
            temp = pre_element_value.get(active_element_name)
            if type(temp) == list:
                # 是数组，追加当前元素内容
                temp.append(active_element[active_element_name])
            else:
                # 是字典，合并两个元素内容为数组
                pre_element_value[active_element_name] = [temp, active_element[active_element_name]]
        # 再将当前元素替换为最顶元素
        self.__active_element = pre_element

    @property
    def xml(self):
        return self.__active_element

    @classmethod
    def __process_inputted_string(cls, input_):
        """
        对输入的值进行处理
        """
        inputted = input_
        outputted = ""
        # 定义标志位，指示上一个字符是斜杠吗？
        is_slash_the_last_char = False
        for single in list(inputted):
            if is_slash_the_last_char:
                # 是斜杠
                if single == "\\":
                    outputted += "\\"
                elif single == "t":
                    outputted += "\t"
                elif single == "n":
                    outputted += "\n"
                else:
                    outputted += "\\" + single
                is_slash_the_last_char = False
            else:
                # 不是斜杠
                if single == "\\":
                    is_slash_the_last_char = True
                else:
                    outputted += single
        return outputted

    @classmethod
    def __process_dict(cls, d: dict):
        """
        处理字典
        """
        if d is None:
            return None
        n_d = dict()
        for key, value in d.items():
            # 对每个字典值进行处理
            n_d[key] = cls.__process_inputted_string(value)
        return n_d

    @classmethod
    def __is_contains_the_key_of_sql(cls, string: str):
        """
        是否包含sql关键字
        """
        text = string.lower()
        if "select" in text:
            return True
        if "update" in text:
            return True
        if "delete" in text:
            return True
        if "insert" in text:
            return True
        return False


class XmlParser(object):
    """
    xml 解析器
    """

    def __init__(self, xml_file: str):
        """
        xml 解析器
        :param xml_file: 需要解析的xml文件
        :return: None
        """
        self.__xml_file = xml_file

    def parse_xml(self) -> dict:
        """
        取得xml解析的结果
        :return: 由xml文件构成的字典值
        """
        parser = make_parser()
        parser.setFeature(feature_namespaces, 0)
        handler = XmlHandler()
        parser.setContentHandler(handler)
        try:
            parser.parse(self.__xml_file)
        except Exception as e:
            raise Exception("解析xml文件[{}]错误，错误原因：{}".format(self.__xml_file, str(e)))
        return handler.xml
