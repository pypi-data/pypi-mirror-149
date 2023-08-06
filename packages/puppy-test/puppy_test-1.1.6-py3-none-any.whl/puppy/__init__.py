__version__ = "1.1.6"

import re
import warnings

import requests

version_re = re.compile("\d+\.\d+\.\d+")

env = None


def check_env():
    """检查位于云桌面还是外网"""
    global env
    if env != None:
        return env
    try:
        r = requests.get("https://mirrors.aliyun.com/pypi/simple/puppy-test", timeout=2)
        if r.status_code == 200:
            env = 2
    except:
        try:
            r = requests.get("http://172.32.4.219/rep/simple/puppy-test", timeout=2)
            if r.status_code == 200:
                env = 1
        except:
            env = 3
    return env



def get_index_and_host():
    if (check_env() == 1):
        return "http://172.32.4.219/rep/simple", "172.32.4.219"
    if (check_env() == 2):
        return "https://mirrors.aliyun.com/pypi/simple", "mirrors.aliyun.com"
    return None, None


def to_int(version):
    """将版本号变为整数"""
    a = version.replace(".", "")
    return int(a)


def get_server_version() -> str:
    """从服务器取到最新的版本"""
    global version_re
    index, host = get_index_and_host()
    if index != None:
        version="0.0.0"
        r = requests.get("{}/puppy-test".format(index), timeout=2)
        for line in r.text.split("\n"):
            fined = version_re.findall(line)
            if len(fined) < 2:
                continue
            if to_int(fined[0])>to_int(version):
                version=fined[0]
        return version
    return get_version()


def get_version() -> str:
    """获取当前框架版本"""
    global __version__
    return __version__


def check_version(version):
    """检查版本"""
    if to_int(version) > to_int(get_version()):
        warnings.warn("当前puppy_test框架版本落后于工程版本，请升级puppy_test框架！", UserWarning)
    if to_int(version) < to_int(get_version()):
        warnings.warn('puppy_test框架版本高于当前工程版本，请使用puppy update命令更新工程！', UserWarning)

