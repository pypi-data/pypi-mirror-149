import base64
import builtins
import hashlib
import os
import random
import string
import time
from ..cfg.config import config
from ..parse.json_parse import JsonParse


def int(o):
    """转型为int"""
    return builtins.int(builtins.float(o))


def float(o):
    """转型为float"""
    return float(o)


def str(o):
    """转型为str"""
    return builtins.str(o)


def bool(o):
    """转型为bool"""
    return builtins.bool(o)


def len(o):
    """获得对象的长度"""
    return builtins.len(o)


def type(o):
    """获得数据的类型"""
    return builtins.type(o)


def loads(json_str):
    """将json字符串转为json对象"""
    json = JsonParse.to_json(json_str)
    if json is None:
        raise Exception("[{}]不是正确的json字符串".format(json))
    return json


def dumps(o):
    """将json对象转为json字符串"""
    return JsonParse.to_good_json_str(o)


def random_letter_and_number(length: int):
    """取得指定长度的随机字母和数字的组合"""
    s = [random.choice(string.ascii_letters + string.digits) for _ in range(length)]
    s = ''.join(s)
    return s


def random_number(length: int):
    """取得length长的随机数字"""
    s = [random.choice(string.digits) for _ in range(length)]
    s = ''.join(s)
    return s


def slice(s, f, l):
    """对字符串切片(s:待切片字符串,f:左切片数,l:右切片数)"""
    s = str(s)
    return s[f:l]


def joint(*args):
    """拼接字符串"""
    s = ""
    for a in args:
        a = str(a)
        s = "{}{}".format(s, a)
    return s


def now(format_str="%Y%m%d%H%M%S"):
    """取得现在的日期"""
    return time.strftime(format_str)


def get_now_date(year=True, mon=True, day=True, hour=True, min=True, second=True):
    """取得当前日期的字符串"""
    format_str = ""
    if year:
        format_str += "%Y"
    if mon:
        format_str += "%m"
    if day:
        format_str += "%d"
    if hour:
        format_str += "%H"
    if min:
        format_str += "%M"
    if second:
        format_str += "%S"
    return time.strftime(format_str)


def get_list(file: str, compared=None, sk_first=True):
    """从file里读取一行，构成列表并返回，每次读取的数据不会重复,一行的不同字段用英文逗号隔开"""
    s_file = file
    if not file.startswith("/"):
        # 当传入的不是一个完整的路径时,拼接项目根目录
        file = os.path.join(config.get_config("base_path"), file)
    if compared is not None:
        t_path, t_file = os.path.split(compared)
        if t_path == "":
            # 当compared不是空的也不是一个完整的路径时,拼接比较文件
            compared = os.path.join(config.get_config("base_path"), file)
    # 如果file不存在,则抛出异常
    if not os.path.exists(file):
        raise Exception("{}文件不存在。".format(s_file))
    if os.path.isdir(file):
        raise Exception("{}不是一个文件。".format(s_file))
    # 如果compared等于None,拼接compared文件
    if compared is None:
        compared = "{}.compared".format(file)
    # 完整读取compared文件,并存入列表
    if not os.path.exists(compared):
        open(compared, "w", encoding="utf-8").close()
    with open(compared, "r", encoding="utf-8") as f:
        compared_l = f.readlines()
    # 按行读取file文件,并判断file的某行是否存在于compared_l,如果存在则读取下一行,直到文件末尾
    with open(file, encoding="utf-8") as f:
        line = f.readline()
        if sk_first:
            line = f.readline()
        if line is None or line == "":
            raise Exception("{}没有可用的测试数据".format(s_file))
        while line in compared_l:
            line = f.readline()
            if line is None or line == "":
                raise Exception("{}已经没有可用的测试数据".format(s_file))
        # 将读取出来的数据追加到compared
        with open(compared, "a", encoding="utf-8") as compared_file:
            compared_file.write(line)
    return line.strip().split(",")


def get_dict(file: str, compared=None):
    """从file里读取一行，构成字典并返回，每次读取的数据不会重复,一行的不同字段用英文逗号隔开"""
    # 从文件中读取数据,将会以第一行为字典健。
    s_file = file
    if not file.startswith("/"):
        # 当传入的不是一个完整的路径时,拼接项目根目录
        file = os.path.join(config.get_config("base_path"), file)
    if compared != None:
        t_path, t_file = os.path.split(compared)
        if t_path == "":
            # 当compared不是空的也不是一个完整的路径时,拼接比较文件
            compared = os.path.join(config.get_config("base_path"), file)
    # 如果file不存在,则抛出异常
    if not os.path.exists(file):
        raise Exception("{}文件不存在。".format(s_file))
    if os.path.isdir(file):
        raise Exception("{}不是一个文件。".format(s_file))
    # 如果compared等于None,拼接compared文件
    if compared is None:
        compared = "{}.compared".format(file)
    # 完整读取compared文件,并存入列表
    if not os.path.exists(compared):
        open(compared, "w", encoding="utf-8").close()
    with open(compared, "r", encoding="utf-8") as f:
        compared_l = f.readlines()
    # 按行读取file文件,并判断file的某行是否存在于compared_l,如果存在则读取下一行,直到文件末尾
    with open(file, encoding="utf-8") as f:
        key_line = f.readline()
        line = f.readline()
        if line is None or line == "":
            raise Exception("{}没有可用的测试数据".format(s_file))
        while line in compared_l:
            line = f.readline()
            if line is None or line == "":
                raise Exception("{}已经没有可用的测试数据".format(s_file))
        # 将读取出来的数据追加到compared
        with open(compared, "a", encoding="utf-8") as compared_file:
            compared_file.write(line)
    # 组合key_line和line
    # a,b,c,d
    # 1,2,3,4
    keys = key_line.strip().split(",")
    values = line.strip().split(",")
    t_dict = {}
    for i in range(len(keys)):
        t_dict[keys[i]] = values[i]
    return t_dict


def path_join(a, b):
    """拼接目录"""
    return os.path.join(a, b)


def base64image(image: str):
    """将图片文件转为base64(image:图片路径)"""
    if not image.startswith("/"):
        image = os.path.join(config.get_config("base_path"), image)
    if not os.path.exists(image):
        raise Exception("待转码文件不存在,文件路径为:{}".format(image))
    with open(image, "rb") as f:
        base64_image = base64.b64encode(f.read()).decode()
    return base64_image


def sleep(wait):
    """睡眠wait秒"""
    time.sleep(wait)


def SHA1(o):
    """SHA1加密"""
    hash_new = hashlib.sha1()
    hash_new.update(str(o).encode("utf8"))
    hash_value = hash_new.hexdigest()
    # print(type(hash_value))
    hash_value = hash_value.upper()  # 转换为大写
    # print(hash_value)
    return hash_value


def MD5(o):
    """对pwd进行md5加密"""
    m = hashlib.md5()
    m.update(str(o).encode("utf-8"))
    return m.hexdigest()


def round(o, ndigits=2):
    """四舍五入"""
    return builtins.round(o, ndigits)
