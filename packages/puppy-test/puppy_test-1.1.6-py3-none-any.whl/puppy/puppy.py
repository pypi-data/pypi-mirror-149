import re
import zipfile
import puppy as _puppy
import shutil
import os
import unittest
import ctypes, sys
from .core.function.string.string_eplace_by_domains import StringReplaceByDomains
from .core.function.utils.params_proc import TransTextToXml

# 取到命令
params = sys.argv[1:]
command = " ".join(params)
# 取到当前项目目录
cwd = os.path.join(os.getcwd())
# 取到puppy的static目录
puppy_path = _puppy.__path__[0]
static_path = os.path.join(puppy_path, "static")
# 取到unittest的目录
unittest_path = unittest.__path__[0]

# 删除意外生成的文件
del_file_name = os.path.join(cwd, "file")


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def exec_by_admin(file):
    if sys.version_info[0] == 3:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, file, None, 1)
    else:
        raise Exception("python版本不受支持!")


def move_unittest_main():
    import unittest
    # 取到puppy的static目录
    puppy_path = _puppy.__path__[0]
    static_path = os.path.join(puppy_path, "static")
    # 取到unittest的目录
    unittest_path = unittest.__path__[0]
    # 替换默认的main.py
    # 先备份
    tmp_file = os.path.join(unittest_path, "tmp.txt")
    try:
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        with open(tmp_file, mode="w") as f:
            pass
    except:
        # 无权限，调用管理员模式
        exec_by_admin(os.path.join(static_path, "move_main.py"))
    else:
        # 有权限
        if os.path.exists(tmp_file):
            os.remove(tmp_file)
        src_main_file = os.path.join(static_path, "main.py")
        main_file = os.path.join(unittest_path, "main.py")
        new_main_file = os.path.join(unittest_path, "main.py.backup")
        if os.path.exists(new_main_file):
            os.remove(new_main_file)
        if os.path.exists(main_file):
            shutil.copy(main_file, new_main_file)
            os.remove(main_file)
        shutil.copy(src_main_file, main_file)


def __unzip(zip_file, dst="."):
    '''
    '''
    if dst == ".":
        dst = os.path.dirname(zip_file)
    with zipfile.ZipFile(file=zip_file, mode='r') as zf:
        for old_name in zf.namelist():
            # 由于源码遇到中文是cp437方式，所以解码成gbk，windows即可正常
            new_name = old_name.encode('cp437').decode('gbk')
            new_path = os.path.join(dst, new_name)
            if old_name.endswith("/"):
                if not os.path.exists(new_path):
                    os.makedirs(new_path)
            else:
                if not os.path.exists(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))
                with open(file=new_path, mode='wb') as f:
                    f.write(zf.read(old_name))


def __install_puppy_plugin():
    """
    安装插件
    :return:
    """
    app_data_path = os.environ["APPDATA"]
    jet_brains_path = os.path.join(app_data_path, "jetBrains")
    start_of_available_version = 20201
    end_of_available_version = 20211
    # 找到pycharm目录
    dir_list = list()
    for root, dirs, files in os.walk(jet_brains_path):
        for dir in dirs:
            if "PyCharm" in dir:
                # 取得版本号
                version = dir[7:]
                # 删除.
                int_type_of_version = _puppy.to_int(version)
                if start_of_available_version <= int_type_of_version <= end_of_available_version:
                    # 说明是受支持的pycharm
                    # 替换文件
                    pycharm_path = os.path.join(root, dir)
                    dir_list.append(pycharm_path)
    # 找到puppy插件安装包
    puppy_plugin_path = None
    puppy_plugin_name = None
    for root, dirs, files in os.walk(cwd):
        for file in files:
            if "PuppyPlugin-" in file:
                puppy_plugin_path = os.path.join(root, file)
                puppy_plugin_name, _ = os.path.splitext(file)
        break
    flag = None
    # 先删除已存在的PuppyPlugin
    for pycharm_path in dir_list:
        puppy_plugin_path_in_pycharm = os.path.join(pycharm_path, "plugins", "PuppyPlugin")
        if os.path.exists(puppy_plugin_path_in_pycharm):
            # 判断其版本是否一致
            if os.path.exists(os.path.join(puppy_plugin_path_in_pycharm, "lib", "{}.jar".format(puppy_plugin_name))):
                continue
            shutil.rmtree(puppy_plugin_path_in_pycharm)
        # 替换新的插件
        flag = True
        __unzip(puppy_plugin_path, os.path.join(pycharm_path, "plugins"))
    # 重启pycharm
    if flag:
        print("\n请手动重启pycharm使插件生效！")
    # 删除临时文件
    os.remove(puppy_plugin_path)


def init(_type):
    if _type == "auto":
        exclude_file = "unit"
    else:
        exclude_file = "auto"
    global params, command, cwd, puppy_path, static_path, unittest_path
    file_path = os.path.join(cwd, "file")
    runner_path = os.path.join(cwd, "runner.py")
    if os.path.exists(file_path) or os.path.exists(runner_path):
        print("警告：当前工程已初始化！继续操作将会覆盖原有文件!如需继续请输入y，退出请输入其他字符\n")
        _i = input("请输入:")
        if _i not in ['y', 'Y']:
            print("终止操作！")
            exit(0)
    # 判断是否存在file文件夹或runner.py
    print("正在创建interface文件夹，并生成一个示例接口XML")
    print("正在创建flow文件夹，并生成一个示例流程XML")
    print("正在创建file/conf文件夹，并生成一个默认配置")
    print("正在创建file/xsd文件夹，并生成接口、流程、案例XML的语法约束文件")
    print("正在创建test_data文件夹，并生成一个示例案例XML")
    print("正在创建test_case模块，并生成一个示例案例XML对应的执行py文件")
    print("正在创建git版本控制忽略文件")
    print("正在创建puppy框架的自述文件")
    print("正在创建runner.py用于案例执行")
    print("正在替换Python单元测试框架UnitTest的main.py用于支持单个案例执行")
    print("正在安装pycharm的puppy插件")
    # 将static目录里的文件拷贝到当前项目
    files = list()
    for _root, _dirs, _files in os.walk(static_path):
        for _f in _files:
            files.append(os.path.join(_root, _f).replace(static_path + "\\", ""))
    for _f in files:
        dst = os.path.join(cwd, _f)
        # 包含main.py文件将不会被拷贝
        if exclude_file in _f:
            continue
        if "main.py" in _f:
            continue
        if "uncopy" in _f:
            continue
        if os.path.exists(dst):
            os.remove(dst)
        if not os.path.exists(os.path.dirname(dst)):
            os.makedirs(os.path.dirname(dst))
        src = os.path.join(static_path, _f)
        shutil.copy(src, dst)
    # 解压文件
    auto_zip = os.path.join(cwd, "{}.zip".format(_type))
    __unzip(auto_zip)
    os.remove(auto_zip)
    # 移动快捷转接口xml文件
    src_file = os.path.join(static_path, "uncopy", "transInterfaceTextToXml.py")
    new_file = os.path.join(cwd, "interface", "transInterfaceTextToXml.py")
    new_path = os.path.dirname(new_file)
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    if os.path.exists(new_file):
        os.remove(new_file)
    shutil.copy(src_file, new_file)
    # 移动main.py文件
    move_unittest_main()
    print("操作已完成！")
    # 安装插件
    __install_puppy_plugin()


def update():
    # 从runner.py取得版本
    number_re = re.compile("\d+\.\d+\.\d+")
    runner_path = os.path.join(cwd, "runner.py")
    now_version = "0.0.0"
    if not os.path.exists(runner_path):
        print("初次操作，请使用puppy init命令进行初始化！")
        return -1
    with open(runner_path, "r", encoding="utf-8") as file:
        for line in file.readlines():
            if "__version__" in line:
                number = number_re.findall(line)
                if len(number) == 0:
                    print("版本信息已被删除，无法继续执行升级！")
                    return -1
                now_version = number[0]
                break
    if _puppy.to_int(now_version) > _puppy.to_int(_puppy.get_version()):
        print("当前工程版本高于puppy-test框架版本，请使用以下命令升级：\n     pip3 install -U puppy-test -i http://172.32.4.219/rep/simple/ "
              "--trusted-host 172.32.4.219")
        return -1
    print("警告：该命令执行过程中请勿强制终止，否则可能导致文件损坏！如需继续请输入y，退出请输入其他字符\n")
    _i = input("请输入：")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        return 0
    # 移动main.py文件
    move_unittest_main()
    print("当前工程的版本:{}".format(now_version))
    foot_update(now_version)
    # 移动文件
    # 文件检查列表
    check_file_list = [os.path.join("file", "conf", "config.cfg"),
                       os.path.join("file", "xsd", "flow.xsd"),
                       os.path.join("file", "xsd", "interface.xsd"),
                       os.path.join("file", "xsd", "scene.xsd"),
                       os.path.join("file", "func.py"),
                       "runner.py"]
    # 检查关键性文件是否存在
    for _f in check_file_list:
        now_file = os.path.join(cwd, _f)
        static_file = os.path.join(static_path, _f)
        if not os.path.exists(now_file):
            now_file_path = os.path.dirname(now_file)
            if not os.path.exists(now_file_path):
                os.makedirs(now_file_path)
            shutil.copy(static_file, now_file)
    # 替换xsd文件,runner文件
    replace_file_list = [os.path.join("file", "xsd", "flow.xsd"),
                         os.path.join("file", "xsd", "interface.xsd"),
                         os.path.join("file", "xsd", "scene.xsd"),
                         "runner.py"]
    for _f in replace_file_list:
        static_file = os.path.join(static_path, _f)
        new_file = os.path.join(cwd, _f)
        new_file_path = os.path.dirname(new_file)
        if not os.path.exists(new_file_path):
            os.makedirs(new_file_path)
        if os.path.exists(new_file):
            os.remove(new_file)
        shutil.copy(static_file, new_file)
    # 替换puppy插件
    puppy_plugin_path = None
    for root, dirs, files in os.walk(os.path.join(static_path)):
        for file in files:
            if "PuppyPlugin" in file:
                puppy_plugin_path = os.path.join(root, file)
                break
        if puppy_plugin_path:
            break
    if puppy_plugin_path:
        shutil.copy(puppy_plugin_path, cwd)
    print("操作已完成！")
    __install_puppy_plugin()
    return 0


def clean():
    """
    清理工程
    :return:
    """
    # 先遍历test_case文件下的py文件名称，判断test_data内是否存在，如果存在则不操作，不存在则删除
    print("该命令可能删除原文件!如需继续请输入y，退出请输入其他字符\n")
    _i = input("请输入：")
    if _i not in ['y', 'Y']:
        print("终止操作！")
        return 0
    path = os.path.join(cwd, "test_case")
    if os.path.exists(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                name, _ = os.path.splitext(file)
                xml_name = os.path.join(cwd, "test_data", "{}.xml".format(name))
                if not os.path.exists(xml_name):
                    os.remove(os.path.join(root, file))
                    print("已移除无效PY文件：{}".format(file))


def generate():
    """
    生成案例
    :return:
    """
    print("敬请期待!")


def other(is_help=False):
    server_version = _puppy.get_server_version()
    now_version = None
    runner_path = os.path.join(cwd, "runner.py")
    number_re = re.compile("\d+\.\d+\.\d+")
    if os.path.exists(runner_path):
        with open(runner_path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                if "__version__" in line:
                    number = number_re.findall(line)
                    if len(number) == 0:
                        break
                    now_version = number[0]
                    break
    desc = ""
    if server_version is not None and _puppy.to_int(server_version) > _puppy.to_int(_puppy.get_version()):
        index, host = _puppy.get_index_and_host()
        desc += "        请使用以下命令升级puppy-test框架:\n          pip3 install -U puppy-test -i {} --trusted-host {}\n\n".format(
            index, host)
    if now_version is not None and _puppy.to_int(now_version) < _puppy.to_int(_puppy.get_version()):
        desc += "        请使用puppy update命令升级当前工程版本！\n"
    if is_help:
        print("帮助：")
    else:
        print("命令输入错误！")
    print(''' 
    1、puppy init：                    初始化工程，仅在新建空工程时使用
    2、puppy update：                  升级当前工程版本
    3、puppy clean：                   清理当前工程无用的文件（如test_case下未使用的py)
    4、puppy translate -f file.txt：   将file.txt文件转为框架可用的xml接口文件，file.txt来源于swagger
    6、puppy record：                  打印puppy-test框架版本记录
    5、puppy create_case -i 接口名 -f 字段名 -r 构建规则：  自动生成测试案例（敬请期待!）
    7、puppy help:                     帮助
    8、puppy version                   版本信息
    
    我们的帮助文档正式上线，可前往 http://172.32.4.219/docs/html/index.html（内网）查阅''')
    if desc != "":
        print("\n提示：\n\n{}".format(desc))


def get_interface_from_swagger_txt(file_name):
    global cwd
    if not os.path.exists(file_name):
        file_path = os.path.join(cwd, file_name)
    else:
        file_path = file_name
    if not os.path.exists(file_path):
        print("文件不存在！")
        exit(-1)
    TransTextToXml(api_file_name=file_path).write_file()
    print("生成成功！")


def log():
    print('''更新日志：
    v0.2.8   2022年1月17日
    1、新增了swagger txt文档转接口xml的功能 
    
    v0.3.4   2022年1月18日
    1、现在while和if标签的ex属性所说明的表达式必须使用${}包围
    2、expect标签新增了var_type属性，用于强制对实际值进行转型
    
    v0.3.5   2022年1月20日
    1、现在框架抛出的错误会直接给出具体在xml文档中出错的位置
    
    v1.1.4 2022年5月6日
    1、支持环境切换
    ''')


def version():
    print("本地框架版本为：{}".format(_puppy.get_version()))
    server_version = _puppy.get_server_version()
    if server_version is not None and server_version != _puppy.get_version():
        print("服务器框架版本为：{}".format(server_version))
    if server_version is not None and _puppy.to_int(server_version) > _puppy.to_int(_puppy.get_version()):
        index, host = _puppy.get_index_and_host()
        print("请使用以下命令升级puppy-test框架:\n          pip3 install -U puppy-test -i {} --trusted-host {}\n\n".format(index,
                                                                                                                host))


def foot_update(now_version):
    version = _puppy.to_int(now_version)
    if version == 0:
        # 从0开始升级
        print("脚本版本已更新至0.0.1")
        version = 1
        # 删除core文件夹
        core_path = os.path.join(cwd, "core")
        if os.path.exists(core_path):
            shutil.rmtree(core_path)
        # 删除plugins文件夹
        plugins_path = os.path.join(cwd, "plugins")
        if os.path.exists(plugins_path):
            shutil.rmtree(plugins_path)
        # 修改test_case文件夹下的内容
        test_case = os.path.join(cwd, "test_case")
        if os.path.exists(test_case):
            for root, dirs, files in os.walk(test_case):
                for file in files:
                    if not file.endswith(".py"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "APIProcessor" not in content:
                            continue
                        content = content.replace("core", "puppy.core")
                        content = content.replace("import unittest", "import unittest, runner")
                        f.truncate()
                        f.seek(0)
                        f.write(content)
        # 修改fun
        fun_path = os.path.join(cwd, "file", "func.py")
        if os.path.exists(fun_path):
            with open(fun_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                content = "".join(lines)
                content = content.replace("from core", "from puppy.core")
                f.seek(0)
                f.write(content)
    if 1 <= version <= 4:
        print("脚本版本已更新至0.0.5")
        version = 5
    if version == 5:
        print("脚本版本已更新至0.0.6")
        version = 6
        # 修改test_data文件夹下的内容
        temp_pattern_1 = re.compile(r">\s*\[\s*]\s*</expect>")
        temp_pattern_2 = re.compile(r">\s*\${\s*\[\s*]\s*}\s*</expect>")
        rep1 = ">\n                    [[]]\n                    </expect>"
        rep2 = ">\n                    ${[[]]}\n                    </expect>"

        def rep(string):
            string = temp_pattern_1.sub(rep1, string)
            string = string.replace("|[]", "|[[]]")
            string = string.replace("|${[]}", "|${[[]]}")
            return temp_pattern_2.sub(rep2, string)

        test_case = os.path.join(cwd, "test_data")
        if os.path.exists(test_case):
            for root, dirs, files in os.walk(test_case):
                for file in files:
                    if not file.endswith(".xml"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "scene" not in content:
                            continue
                        srb = StringReplaceByDomains(["<expect", "</expect>"], 'type="sql"')
                        content = srb.replace(content, rep)
                        f.truncate()
                        f.seek(0)
                        f.write(content)
    if 6 <= version <= 27:
        print("脚本版本已更新至0.2.8")
        version = 28
    if version == 28:
        # 将translnterfaceTextToXml.py复制到当前项目的interface目录下
        src_file = os.path.join(static_path, "uncopy", "transInterfaceTextToXml.py")
        new_file = os.path.join(cwd, "interface", "transInterfaceTextToXml.py")
        new_path = os.path.dirname(new_file)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        if os.path.exists(new_file):
            os.remove(new_file)
        shutil.copy(src_file, new_file)
        print("脚本版本已更新至0.2.9")
        version = 29
    if 29 <= version <= 30:
        print("脚本版本已更新至0.3.1")
        version = 31
    if version == 31:
        # 修改test_data文件夹下的内容
        pattern_1 = re.compile("ex='([\S\s]*?)'")
        pattern_2 = re.compile('ex="([\S\s]*?)"')

        def rep_3_1(string):
            group1 = pattern_1.findall(string)
            if len(group1) == 1:
                old = group1[0]
                new = "${{{}}}".format(old)
                string = string.replace(old, new)
            group2 = pattern_2.findall(string)
            if len(group2) == 1:
                old = group2[0]
                new = "${{{}}}".format(old)
                string = string.replace(old, new)
            return string

        test_data = os.path.join(cwd, "test_data")
        if os.path.exists(test_data):
            for root, dirs, files in os.walk(test_data):
                for file in files:
                    if not file.endswith(".xml"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "scene" not in content:
                            continue
                        srb = StringReplaceByDomains(["<while", ">"], 'ex')
                        content = srb.replace(content, rep_3_1)
                        srb = StringReplaceByDomains(["<if", ">"], 'ex')
                        content = srb.replace(content, rep_3_1)
                        f.truncate()
                        f.seek(0)
                        f.write(content)
        print("脚本版本已更新至0.3.2")
        version = 32
    if 32 <= version <= 100:
        print("脚本版本已更新至1.0.1")
        version = 101
    if version == 101:
        # 修改test_data文件夹下的内容
        pattern_key = re.compile("(key\s*=)['\"]")
        pattern_items = re.compile("(items\s*=)['\"]")

        def rep_1_0_1(string):
            group_key = pattern_key.findall(string)
            if len(group_key) == 1:
                old = group_key[0]
                new = "name="
                string = string.replace(old, new)
            group_items = pattern_items.findall(string)
            if len(group_items) == 1:
                old = group_items[0]
                new = "data="
                string = string.replace(old, new)
            return string

        test_data = os.path.join(cwd, "test_data")
        if os.path.exists(test_data):
            for root, dirs, files in os.walk(test_data):
                for file in files:
                    if not file.endswith(".xml"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "scene" not in content:
                            continue
                        srb = StringReplaceByDomains(["<for", ">"], 'key')
                        content = srb.replace(content, rep_1_0_1)
                        f.truncate()
                        f.seek(0)
                        f.write(content)
        print("脚本版本已更新至1.0.2")
        version = 102
    if version == 102:
        # 修改test_data文件夹下的内容
        pattern_ex = re.compile(r"=\s*(\${[\s\S]*?})")
        replace_ex = re.compile(r"=\s*")

        def rep_1_0_2(string):
            iter = pattern_ex.finditer(string)
            results = list()
            for matcher in iter:
                start = matcher.start()
                end = matcher.end()
                source = matcher.group()
                source = replace_ex.sub("='", source)
                result = "{}'".format(source)
                results.append({"start": start, "end": end, "result": result})
            offset = 0
            for _r in results:
                start = _r.get("start") + offset
                end = _r.get("end") + offset
                result = _r.get("result")
                offset += len(result) - (end - start)
                pre = string[:start]
                post = string[end:]
                string = "{}{}{}".format(pre, result, post)
            return string

        test_data = os.path.join(cwd, "test_data")
        if os.path.exists(test_data):
            for root, dirs, files in os.walk(test_data):
                for file in files:
                    if not file.endswith(".xml"):
                        continue
                    file_name = os.path.join(root, file)
                    with open(file_name, "r+", encoding="utf-8") as f:
                        lines = f.readlines()
                        content = "".join(lines)
                        if "scene" not in content:
                            continue
                        srb = StringReplaceByDomains(["sql", ">"], "=")
                        content = srb.replace(content, rep_1_0_2)
                        f.truncate()
                        f.seek(0)
                        f.write(content)
        print("脚本版本已更新至1.0.3")
        version = 103
    if 103 <= version <= 109:
        print("脚本版本已更新至1.1.0")
        version = 110
    if version == 110:
        config_path = os.path.join(cwd, "file", "conf", "config.cfg")
        if os.path.exists(config_path):
            with open(config_path, "r+", encoding="utf-8") as f:
                lines = f.readlines()
                content = "".join(lines)
                if "[DEFAULT]" in content:
                    content = content.replace("[DEFAULT]", "[config]")
                f.truncate()
                f.seek(0)
                f.write(content)
            print("脚本版本已更新至1.1.1")
        version = 111
    if 111 <= version <= 115:
        print("脚本版本已更新至1.1.6")
        version = 116


def main():
    global command
    command = command.replace(" ", "")
    if command == "init-tunit" or command == "init":
        init("unit")
    elif command == "init-tauto":
        init("auto")
    elif command == "update":
        update()
    elif command == "clean":
        clean()
    elif "create_case" in command:
        generate()
    elif "translate-f" in command:
        file_name = command[11:]
        print(file_name)
        get_interface_from_swagger_txt(file_name)
    elif command == "help":
        other(True)
    elif command == "record":
        log()
    elif command in ["version", "-v"]:
        version()
    else:
        other()
