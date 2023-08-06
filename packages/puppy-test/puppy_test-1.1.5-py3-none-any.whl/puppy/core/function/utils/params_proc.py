# -*- coding:utf-8
from xml.dom.minidom import Document
import os
import json

class ExtractData():
    '''从txt文件中提取url,body'''
    def __init__(self, api_file_name):
        self.text_name = '{}.txt'.format(api_file_name)

    def params_to_body(self):
        '''
        读取swagger参数，提取body
        :return: url:str, body:dict
        '''
        with open(self.text_name, "r", encoding='utf-8') as f:
            data_list = f.readlines()
            data_list = [x.strip() for x in data_list if x.strip() != '']  # 过滤空行，去掉非空行首尾的空格
            self.module_name = data_list[1].split("`")[1].split('/')[1]
            self.url = data_list[1].split("`")[1].split(self.module_name)[1]  # 获取url
            # params保存从具体参数字段开始的所有数据
            params = data_list[9:]
            # params_list保存具体参数字段到 响应状态 之间的所有行数据
            params_list = []
            for i in range(len(params)):
                if params[i] == '**响应状态**':
                    break
                else:
                    params_list.append(params[i])

            params_name_list = [p.split('|')[1].strip() for p in params_list]  # 所有请求参数字段名
            type_list = [p.split('|')[5].strip() for p in params_list]  # 所有请求参数类型名
            is_need_list = [p.split('|')[4].strip() for p in params_list]  # 所有请求参数是否必须

            self.body = dict(zip(params_name_list, is_need_list))
            return self.url, self.body

class TransTextToXml():
    '''生成xml文件'''
    def __init__(self, api_file_name):
        self.__file = api_file_name.split('.')[0]
        self.file_xml = '{}.xml'.format(self.__file)
        self.base_inventory = os.getcwd()
        self.file_xml = os.path.join(self.base_inventory, self.file_xml)
        self.protocol = 'http'
        self.method = 'post'
        self.desc = self.__file
        self.url = self.get_data()[0]
        self.body = self.get_data()[1]
        self.content = {}


    def get_data(self):
        ed = ExtractData(api_file_name=self.__file)
        self.url, self.body = ed.params_to_body()
        return self.url, self.body

    def write_file(self):
        fp = open(self.file_xml, 'w',encoding="utf-8")
        self.interface ='''<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<interface xmlns=\"http://www.w3school.com.cn\"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://www.w3school.com.cn ../file/xsd/interface.xsd"
           protocol="{}" method="{}" desc="{}">'''.format(self.protocol, self.method, self.desc)

        self.server_port_xml = '''\n\t<server>${server}</server>\n\t<port>${port}</port>'''
        self.path_xml = '''\n\t<path>{}</path>'''.format(self.url)
        self.header_xml = '''\n\t<header>\n\t\t{\n\t\t\t"imei":"353114008878656",\n\t\t\t"appversion":"3.0.0.1",\n\t\t\t"Content-Type":"application/json"\n\t\t}\n\t</header>'''

        self.interface_label = '''\n</interface>'''
        self.body = json.dumps(self.body)
        self.body_xml = '''\n\t<body type="json">\n\t\t{}\n\t</body>'''.format(self.body)
        content = self.interface + self.server_port_xml+self.path_xml+self.header_xml +self.body_xml+self.interface_label

        '''body数据未做处理，原始数据直接转'''
        self.body = json.loads(self.body)
        fp.write(content)


if __name__ == "__main__":
    t = TransTextToXml(api_file_name='addTransferPlan_api.txt')
    t.write_file()
