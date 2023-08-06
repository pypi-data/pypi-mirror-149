# -*- coding:utf-8 -*-
"""
    author: Li Junxian
    function:is used to calculate for $ expression
    在配置文件里的计算：已读取变量>已读取配置
    在接口文件里的计算：自定义模块>已读取变量（生效的环境）>已读取配置
    在案例和流程文件里的计算：局部变量>自定义模块>已读取变量（生效的环境）>已读取配置
"""
import re
from decimal import Decimal

from ..utils.utils import Utils
from ...exception.my_exception import MyException
from ...function.func.module import Module, inner, outer


class ParamType(object):
    """
    判断字符串是什么类型的数据
    """
    __str = "str"
    __int = "int"
    __float = "float"
    __bool = "bool"
    # 支持的运算符正则
    __operator_re = re.compile(
        r"(\+)|(-)|(not)|(or)|(and)|(\*)|(/)|(%)|(==)|(<=)|(>=)|(<)|(>)|(!=)|(\[)|(\()|(\))|(:)|(in)|(not in)|(\.)|(->)")
    # 支持的操作数正则
    __operand_re = re.compile(r"('[\s\S]*?')|(-?\d+\.\d*)|(-?\d+)|(False)|(True)|(false)|(true)|(None)|(null)")
    # 变量的正则
    __var_re = re.compile(r"((\w\.?)+)")
    # 特殊变量的正则
    __s_var_re = re.compile(r"(-(\w\.?)+)")
    # 直接从模块里读取的函数或对象的名称正则
    __o_var_re = re.compile(r"(\+(\w\.?)+)")
    # 字符串的正则
    __str_re = re.compile(r"('[\s\S]*?')")
    # 小数的正则
    __float_re = re.compile(r"(-?\d+\.\d*)")
    # 整数的正则
    __int_re = re.compile(r"(0)|(-?[1-9]\d*)")
    # 布尔的正则
    __bool_re = re.compile(r"(False)|(True)|(false)|(true)")
    # 方法的正则
    __method_re = re.compile(r"^(?P<name>\w[\w,_\d]*)\((?P<params>.*)\)$")
    # 方法名的正则
    __method_name_re = re.compile(r"^(\w[\w_\d]*)$")
    # None的正则
    __none_re = re.compile(r"(None)|(null)")

    @classmethod
    def is_operator(cls, param: str):
        """
        是运算符吗？
        :param param:
        :return:
        """
        return cls.__operator_re.fullmatch(param) is not None

    @classmethod
    def is_operand(cls, param: str):
        """
        是操作数吗？不包含变量
        :param param:
        :return:
        """
        return cls.__operand_re.fullmatch(param) is not None

    @classmethod
    def is_var(cls, param: str):
        """
        是变量吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        if cls.is_operand(param):
            return False
        if cls.is_operator(param):
            return False
        if cls.is_list(param):
            return False
        return cls.__var_re.fullmatch(param) is not None

    @classmethod
    def is_s_var(cls, param: str):
        """
        是特殊变量吗？用来指代.运算符后的变量
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        if cls.is_operand(param):
            return False
        if cls.is_operator(param):
            return False
        if cls.is_list(param):
            return False
        return cls.__s_var_re.fullmatch(param) is not None

    @classmethod
    def is_o_var(cls, param: str):
        """
        是直接调用的对象或者方法的名称吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        if cls.is_operand(param):
            return False
        if cls.is_operator(param):
            return False
        if cls.is_list(param):
            return False
        return cls.__o_var_re.fullmatch(param) is not None

    @classmethod
    def is_un_know(cls, param):
        if cls.is_operand(param):
            return False
        if cls.is_operator(param):
            return False
        if cls.is_var(param):
            return False
        if cls.is_list(param):
            return False
        return True

    @classmethod
    def is_str(cls, param):
        """
        是字符串吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        return cls.__str_re.fullmatch(param) is not None

    @classmethod
    def is_float(cls, param):
        """
        是小数吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        return cls.__float_re.fullmatch(param) is not None

    @classmethod
    def is_int(cls, param):
        """
        是整数吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        return cls.__int_re.fullmatch(param) is not None

    @classmethod
    def is_bool(cls, param):
        """
        是布尔吗？
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        return cls.__bool_re.fullmatch(param) is not None

    @classmethod
    def is_none(cls, param):
        """
        是none类型吗
        :param param:
        :return:
        """
        if type(param) != str:
            param = str(param)
        return cls.__none_re.fullmatch(param) is not None

    @classmethod
    def is_method(cls, param):
        """
        是方法吗？
        :param param:
        :return:
        """
        return cls.__method_re.fullmatch(param) is not None

    @classmethod
    def get_method_name_and_params_str(cls, param):
        """
        取得参数和名字的字符串
        :param param:
        :return:
        """
        res = cls.__method_re.findall(param)
        name = res[0][0]
        params = "({})".format(res[0][1])
        return name, params

    @classmethod
    def to_int(cls, o):
        return int(o)

    @classmethod
    def to_bool(cls, o):
        if o in ["True", "true"]:
            return True
        else:
            return False

    @classmethod
    def to_float(cls, o):
        return float(o)

    @classmethod
    def transform_to_real(cls, param):
        """
        将传入的参数转为其可能的类型的值，如果转换不成功则返回一个空的tuple
        :param param:
        :return:
        """
        if cls.is_var(param):
            return Utils.ERROR
        if cls.is_un_know(param):
            return Utils.ERROR
        if cls.is_none(param):
            return None
        if cls.is_bool(param):
            return cls.to_bool(param)
        if cls.is_int(param):
            return cls.to_int(param)
        if cls.is_float(param):
            return cls.to_float(param)
        if cls.is_str(param):
            return param[1:-1]
        return param

    @classmethod
    def transform_to_str(cls, parma):
        """
        将传入的参数转为字符串，如果本身就是字符串，需要添加单引号
        :param parma:
        :return:
        """
        if type(parma) in [str, dict]:
            return "'{}'".format(parma)
        return str(parma)

    @classmethod
    def is_method_name(cls, param):
        """
        是方法的名字吗？
        :param param:
        :return:
        """
        return cls.__method_name_re.fullmatch(param) is not None

    @classmethod
    def is_list(cls, param):
        return len(param) > 0 and param[0] == "["

    @classmethod
    def is_dict(cls, param):
        return param[0] == "{"


class Express(object):
    """
    表达式处理
    """
    # 空白正则表达式
    __blank_re = re.compile(r"\s")
    # 字母数字下划线的表达式
    __letter_number_re = re.compile(r"[a-zA-Z0-9_]")
    # 字母下划线的表达式
    __letter_re = re.compile(r'[a-zA-Z_]')

    def __init__(self, express):
        """
        :param express:需要处理的表达式
        :type express: str
        """
        if express:
            express = express.strip()
        # 表达式字符串
        self.__express_str = express
        # 中缀表达式列表
        self.__in_express = []
        # 标志表达式是否有误
        self.__error = None
        # 后缀表达式列表
        self.__post_express = []
        # 计算结果
        self.__re = None

    def __process_to_express(self):
        """
        将表达式字符串转为表达式列表
        :return:
        """
        express = self.__express_str.strip()
        # 指示当前是否位于引号
        quotes = False
        # 指示当前处理的是运算符
        operator = False
        # 存储表达式的列表
        expr = list()
        # 创建指示字符串单引号的标志位，初始值为false
        single_quotes_for_str = False
        # 创建指示字符串双引号的标志位，初始值为false
        double_quotes_for_str = False
        # 存储当前处理的
        current = ""
        # 创建指示括号的标志位，初值为0
        parenthesis = 0
        # 指示上一个字符是否是反斜杠
        backslash = False
        # 判断第一个字符是否是运算符
        if express[0] == "-":
            operator = True
        # 判断上一个字符是字母吗
        if express[0] in ["(", "["]:
            letter = False
        else:
            letter = True
        # 指示中括号的数量
        brace = 0
        for e in list(express):
            if e in [" ", "\t", "\n"] and not quotes and brace <= 0 and parenthesis <= 0:
                letter = False
                backslash = False
                operator = False
                if current != "":
                    expr.append(current)
                current = ""
                continue
            elif e == "\\" and not backslash:
                letter = False
                backslash = True
            elif e == "]" and not backslash and not quotes and brace <= 0 and parenthesis <= 0:
                backslash = False
                operator = False
                letter = True
                if current != "":
                    expr.append(current)
                    current = ""
            elif e == "(" and not backslash and not letter and not quotes and brace <= 0 and parenthesis <= 0:
                backslash = False
                operator = False
                letter = False
                if current != "":
                    expr.append(current)
                    current = ""
                expr.append("(")
            elif e == ")" and not backslash and not quotes and brace <= 0 and parenthesis <= 0:
                backslash = False
                operator = False
                letter = False
                if current != "":
                    expr.append(current)
                    current = ""
                expr.append(")")
            elif e == "." and not backslash and not quotes and brace <= 0 and parenthesis <= 0 and letter:
                backslash = False
                operator = False
                letter = False
                if current != "":
                    expr.append(current)
                    current = ""
                expr.append(".")
            elif e == ":" and not backslash and not quotes and brace <= 0 and parenthesis <= 0:
                backslash = False
                operator = False
                letter = False
                if current != "":
                    expr.append(current)
                    current = ""
                expr.append(":")
            else:
                if e in ['"', "'"] and not backslash:
                    if brace <= 0 and parenthesis <= 0 and not quotes:
                        operator = False
                        if current != "":
                            expr.append(current)
                        current = ""
                    if e == "'" and not double_quotes_for_str:
                        single_quotes_for_str = not single_quotes_for_str
                        quotes = single_quotes_for_str
                    elif e == '"' and not single_quotes_for_str:
                        double_quotes_for_str = not double_quotes_for_str
                        quotes = double_quotes_for_str
                        e = "'"
                elif backslash and e not in ['"', "'"]:
                    current += "\\"
                backslash = False
                if e == "(" and letter and not backslash and not quotes and brace <= 0:
                    parenthesis += 1
                if e == ")" and not backslash and not quotes and brace <= 0 and parenthesis > 0:
                    parenthesis -= 1
                if e == "]" and not backslash and not quotes and parenthesis <= 0 and brace > 0:
                    brace -= 1
                if e == "[" and not letter and not backslash and not quotes and parenthesis <= 0:
                    if brace == 0:
                        operator = False
                        if current != "":
                            expr.append(current)
                        current = ""
                    brace += 1
                if e in ["+", "-", "*", "/", "%", ">", "<", "!",
                         "=", "["] and not operator and not quotes and parenthesis <= 0 and brace <= 0:
                    if (e == "[" and letter) or e != "[":
                        operator = True
                        if current != "":
                            expr.append(current)
                        current = ""
                elif operator and not quotes and parenthesis <= 0 and e != "=" and brace <= 0:
                    operator = False
                    if current != "":
                        expr.append(current)
                    current = ""
                if brace <= 0 and parenthesis <= 0 and not quotes:
                    if ")" == e and letter:
                        letter = True
                    else:
                        letter = False
                        if self.__letter_re.fullmatch(e):
                            letter = True
                        elif self.__letter_number_re.fullmatch(e):
                            if ParamType.is_var(current):
                                letter = True
                        elif "[" == e and operator:
                            letter = True
                        elif "]" == e:
                            letter = True
                current += e
        if current != "":
            expr.append(current)
        self.__in_express = expr

    def __process_param(self, param, *context):
        """
        处理参数
        :param context:多个对象，包含字典或者Function对象
        :param param:
        :return:
        """
        if ParamType.is_var(param):
            for _c in context:
                if type(_c) is dict:
                    if param in _c.keys():
                        return _c.get(param)
                if type(_c) is Module:
                    if _c.has_var(param):
                        return _c.var(param)
                    if _c.has_module(param):
                        return _c.module(param)
            raise Exception("未找到标识符 {} 说明的值".format(param))
        elif ParamType.is_s_var(param):
            return param[1:]
        elif ParamType.is_o_var(param):
            n_param = param[1:]
            for _c in context:
                if type(_c) is Module:
                    if _c.has_func(n_param):
                        return _c.func(n_param)
                    if _c.has_class(n_param):
                        return _c.clazz(n_param)
            raise Exception("未在自定义模块和内置模块找到标识符 {} 引用的函数或对象".format(n_param))
        elif ParamType.is_list(param):
            ex_o = Express(param)
            r = ex_o.calculate(*context)
            if r == Utils.ERROR:
                raise Exception("其中的子表达式计算出错，原因为:{}".format(ex_o.error))
            return r
        elif ParamType.is_method(param):
            # 遍历方法的字符，取得名字
            name = ""
            parenthesis = 0
            brace = 0
            params = list()
            active = ""
            blackflash = False
            que = False
            for e in list(param):
                if e == "\\":
                    blackflash = True
                    continue
                if e == "'" and not blackflash:
                    que = not que
                elif blackflash and e != "'":
                    active += "\\"
                if e == "(" and not blackflash and not que:
                    blackflash = False
                    parenthesis += 1
                    if parenthesis == 1:
                        continue
                if e == ")" and not blackflash and not que:
                    blackflash = False
                    parenthesis -= 1
                    if parenthesis == 0:
                        continue
                if e == "[" and not blackflash and not que:
                    brace += 1
                if e == "]" and not blackflash and not que:
                    brace -= 1
                if parenthesis == 0:
                    name += e
                elif (e == ",") and (parenthesis == 1) and (brace == 0) and not blackflash and not que:
                    blackflash = False
                    if active != "":
                        params.append(active)
                        active = ""
                else:
                    blackflash = False
                    active += e
            if active != "":
                params.append(active)
            # 创建一个空的list用来存储已经计算的参数
            calculated_param = []
            # 遍历参数进行取值
            for param in params:
                ex_o = Express(param)
                r = ex_o.calculate(*context)
                if r == Utils.ERROR:
                    raise Exception("其中的子表达式错误，错误原因:{}".format(ex_o.error))
                calculated_param.append(r)
            # 调用方法
            return calculated_param
        else:
            t = ParamType.transform_to_real(param)
            return t

    @property
    def error(self):
        return self.__error

    @staticmethod
    def __get_level_of_operator(operator):
        """
        获得运算符的优先级
        返回None说明不是支持的运算符
        :param operator:
        :return:
        """
        if operator in ["("]:
            return 0
        if operator in [".", "->"]:
            return 10
        if operator in ["in", "not in"]:
            return 8
        if operator in ["[", ":"]:
            return 7
        if operator in ["not"]:
            return 6
        if operator in ["*", "/", "%"]:
            return 5
        if operator in ["+", "-"]:
            return 4
        if operator in ["==", "<=", ">=", "<", ">", "!="]:
            return 3
        if operator in ["and"]:
            return 2
        if operator in ["or"]:
            return 1
        return None

    @staticmethod
    def __get_number_of_operand_of_operator(operator):
        """
        得到操作符的操作数的个数
        :param operator:
        :return:
        """
        if operator == "not":
            return 1
        elif operator == ":":
            return 3
        else:
            return 2

    def __in_ex_to_post_ex(self):
        """
        中缀表达式转后缀表达式
        :return:
        """
        in_expression = self.__in_express
        # 中缀转后缀
        # 中缀表达式
        postfix_expression = []
        # 临时堆栈
        tmp_stack = []
        for in_o in in_expression:
            # 是运算符吗？
            if ParamType.is_operator(in_o):
                # 临时堆栈有运算符吗？
                if in_o == ")":
                    while True:
                        if len(tmp_stack) > 0:
                            t = tmp_stack.pop()
                            if t == "(":
                                break
                            postfix_expression.append(t)
                        else:
                            raise Exception("括号运算符必须是成对的！")
                else:
                    while len(tmp_stack) > 0 and in_o != "(":
                        if in_o == ":" and tmp_stack[-1] == "[":
                            tmp_stack.pop()
                        if len(tmp_stack) > 0:
                            # 取出第一个运算符，判断其优先级是否大于等于in_o,如果大于等于则弹出至后缀表达式
                            if self.__get_level_of_operator(tmp_stack[-1]) >= self.__get_level_of_operator(in_o):
                                postfix_expression.append(tmp_stack.pop())
                            else:
                                break
                    tmp_stack.append(in_o)
            else:
                # 不是运算符
                postfix_expression.append(in_o)
        while len(tmp_stack) > 0:
            postfix_expression.append(tmp_stack.pop())
        self.__post_express = postfix_expression

    def __calculate_post_ex(self, *context):
        """
        计算后缀表达式的值
        :return:
        """
        post_ex = self.__post_express
        # 参数临时堆栈
        tmp_stack = []
        for post in post_ex:
            if not ParamType.is_operator(post):
                # 如果是操作数
                processed_post = self.__process_param(post, *context)
                if processed_post == Utils.ERROR:
                    raise Exception("操作数转换失败，不受支持的运算！")
                tmp_stack.append(processed_post)
            elif ParamType.is_operator(str(post)):
                # 如果是运算符
                # 检查操作数堆栈是否为空，如果为空抛出错误
                tmp_stack_len = len(tmp_stack)
                number_of_operand = self.__get_number_of_operand_of_operator(str(post))
                if tmp_stack_len < number_of_operand:
                    raise Exception("没有足够多的操作数满足运算符 {} !".format(str(post)))
                # 检查运算符的操作数个数
                if number_of_operand == 1:
                    # 弹出一个操作数
                    first = Express.__only_float_to_decimal(tmp_stack.pop())
                    # 是not运算符
                    res = not first
                elif number_of_operand == 3:
                    third = Express.__only_float_to_decimal(tmp_stack.pop())
                    second = Express.__only_float_to_decimal(tmp_stack.pop())
                    first = Express.__only_float_to_decimal(tmp_stack.pop())
                    # 是:运算符
                    res = first[second:third]
                else:
                    # 弹出两个操作数
                    second = Express.__only_float_to_decimal(tmp_stack.pop())
                    first = Express.__only_float_to_decimal(tmp_stack.pop())
                    if post == "*":
                        res = first * second
                    elif post == "/":
                        res = first / second
                    elif post == "%":
                        res = first % second
                    elif post == "+":
                        if type(first) == str or type(second) == str:
                            first = str(first)
                            second = str(second)
                        res = first + second
                    elif post == "-":
                        res = first - second
                    elif post == "==":
                        res = first == second
                    elif post == "<=":
                        res = first <= second
                    elif post == ">=":
                        res = first >= second
                    elif post == "<":
                        res = first < second
                    elif post == ">":
                        res = first > second
                    elif post == "!=":
                        res = first != second
                    elif post == "and":
                        res = first and second
                    elif post == "or":
                        res = first or second
                    elif post == "[":
                        res = first[second]
                    elif post == "in":
                        res = first in second
                    elif post == "not in":
                        res = first not in second
                    elif post == "->":
                        res = first(*second)
                    elif post == ".":
                        if type(first) is dict:
                            res = first["{}".format(second)]
                        else:
                            res = getattr(first, second)
                    else:
                        raise Exception("不受支持的运算符 {} ".format(post))
                tmp_stack.append(Express.__only_decimal_to_float(res))
            else:
                raise Exception("该操作数或运算符 {} 不受支持！".format(post))
        if len(tmp_stack) != 1:
            raise Exception("操作数过多！")
        self.__re = tmp_stack.pop()

    def __calculate_tuple(self, *context):
        """
        计算列表
        """
        express = self.__express_str.strip()
        # 定义个列表栈区
        stack = []
        # 定义一个cursor，指示当前操作位置
        cursor = None
        # 创建指示小括号的标志位，初始值为0
        parenthesis = 0
        # 指示大括号的标志位，初始值为 0
        brace = 0
        # 指示中括号的标志位，初值为 0
        bracket = 0
        # 指示目前是元祖状态
        is_tuple = False
        # 创建指示字符串单引号的标志位，初始值为false
        single_quotes_for_str = False
        # 创建指示字符串双引号的标志位，初始值为false
        double_quotes_for_str = False
        # 创建指示位于引号状态
        quotes = False
        # 指示上一个字符是否是反斜杠
        backslash = False
        # 指示项
        value = ""
        for e in list(express):
            if e == "(" and parenthesis <= 0 and brace <= 0 and bracket <= 0:
                if not ParamType.is_method_name(value):
                    is_tuple = True
            if e in ["\n", "\t", " "] and not quotes and brace <= 0 and bracket <= 0:
                continue
            elif e == "(" and is_tuple and brace <= 0 and bracket <= 0:
                # 遇到左小括号，说明了一个元组结构的开始
                is_tuple = False
                cursor = list()
                stack.append(cursor)
                value = ""
            elif e in [",", ")"] and parenthesis <= 0 and not quotes and brace <= 0 and bracket <= 0:
                if value != "":
                    ex_o = Express(value)
                    r = ex_o.calculate(*context)
                    if r == Utils.ERROR:
                        raise Exception("其中的子表达式错误，错误原因:{}".format(ex_o.error))
                    value = r
                    cursor.append(value)
                value = ""
                if e == ")":
                    if len(stack) >= 2:
                        cursor = stack.pop()
                        parent = stack.pop()
                        parent.append(tuple(cursor))
                        cursor = parent
                        stack.append(parent)
                    else:
                        return tuple(cursor)
            elif e == "\\" and not backslash and brace <= 0 and bracket <= 0:
                backslash = True
            else:
                if e == '"' and not backslash and not double_quotes_for_str:
                    single_quotes_for_str = not single_quotes_for_str
                    quotes = single_quotes_for_str
                if e == "'" and not backslash and not single_quotes_for_str:
                    double_quotes_for_str = not double_quotes_for_str
                    quotes = double_quotes_for_str
                if e == "(" and not backslash and not quotes and brace <= 0 and bracket <= 0:
                    parenthesis += 1
                if e == ")" and not backslash and not quotes and brace <= 0 and bracket <= 0:
                    parenthesis -= 1
                if e == "{" and not backslash and not quotes and bracket <= 0:
                    brace += 1
                if e == "}" and not backslash and not quotes and bracket <= 0:
                    brace -= 1
                if e == "[" and not backslash and not quotes and brace <= 0:
                    bracket += 1
                if e == "]" and not backslash and not quotes and brace <= 0:
                    bracket -= 1
                backslash = False
                value += e
        return tuple(cursor)

    def __calculate_list(self, *context):
        """
        计算列表
        """
        express = self.__express_str.strip()
        # 定义个列表栈区
        stack = []
        # 定义一个cursor，指示当前操作位置
        cursor = None
        # 创建指示小括号的标志位，初始值为0
        parenthesis = 0
        # 指示tuple标志位
        is_tuple = False
        # 指示tuple内左小括号数量
        parenthesis_for_tuple = 0
        # 指示大括号的标志位，初始值为 0
        brace = 0
        # 创建指示字符串单引号的标志位，初始值为false
        single_quotes_for_str = False
        # 创建指示字符串双引号的标志位，初始值为false
        double_quotes_for_str = False
        # 创建指示位于引号状态
        quotes = False
        # 指示上一个字符是否是反斜杠
        backslash = False
        # 指示项
        value = ""
        # 指示上一个字符是否是逗号
        comma = True
        # 指示非结构式中括号数量
        bracket = 0
        for e in list(express):
            if e == "(" and parenthesis <= 0 and brace <= 0:
                if not ParamType.is_method_name(value):
                    is_tuple = True
                    parenthesis_for_tuple += 1
            if e in ["\n", "\t", " "] and not quotes and brace <= 0 and not is_tuple:
                comma = False
                continue
            elif e == "[" and brace <= 0 and not is_tuple and not quotes and comma:
                # 遇到左中括号，说明了一个列表结构的开始
                cursor = list()
                stack.append(cursor)
                value = ""
            elif e in [",", "]"] and parenthesis <= 0 and not quotes and brace <= 0 and not is_tuple and bracket <= 0:
                if value != "":
                    ex_o = Express(value)
                    r = ex_o.calculate(*context)
                    if r == Utils.ERROR:
                        raise Exception("其中的子表达式错误，错误原因:{}".format(ex_o.error))
                    value = r
                    cursor.append(value)
                value = ""
                if e == "]":
                    if len(stack) >= 2:
                        cursor = stack.pop()
                        parent = stack.pop()
                        parent.append(cursor)
                        cursor = parent
                        stack.append(parent)
                    else:
                        return cursor
                else:
                    comma = True
            elif e == "\\" and not backslash and brace <= 0 and not is_tuple:
                comma = False
                backslash = True
            else:
                comma = False
                if e == '"' and not backslash and not double_quotes_for_str:
                    single_quotes_for_str = not single_quotes_for_str
                    quotes = single_quotes_for_str
                if e == "'" and not backslash and not single_quotes_for_str:
                    double_quotes_for_str = not double_quotes_for_str
                    quotes = double_quotes_for_str
                if e == "(" and not backslash and not quotes and brace <= 0 and not is_tuple:
                    parenthesis += 1
                if e == ")" and not backslash and not quotes and brace <= 0 and not is_tuple:
                    parenthesis -= 1
                if e == "{" and not backslash and not quotes and not is_tuple:
                    brace += 1
                if e == "}" and not backslash and not quotes and not is_tuple:
                    brace -= 1
                if e == ")" and is_tuple and brace <= 0 and not quotes and not backslash:
                    parenthesis_for_tuple -= 1
                    if parenthesis_for_tuple <= 0:
                        is_tuple = False
                if e == "[" and not backslash and not quotes and brace <= 0 and not is_tuple:
                    bracket += 1
                if e == "]" and not backslash and not quotes and brace <= 0 and not is_tuple:
                    bracket -= 1
                backslash = False
                value += e
        return cursor

    def __calculate_dict(self, *context):
        """
        计算字典
        {'a':'b','a':b}
        """
        express = self.__express_str.strip()
        # 构造列表项
        # 定义一个字典栈区
        stack = []
        # 定义一个cursor，指示当前操作的位置
        cursor = None
        # 创建指示小括号的标志位，初始值为0
        parenthesis = 0
        # 创建指示中括号的标志位，初始值为0
        bracket = 0
        # 指示tuple标志位
        is_tuple = False
        # 指示tuple内左小括号数量
        parenthesis_for_tuple = 0
        # 创建指示单引号的标志位，初始值为false
        single_quotes = False
        # 创建指示字符串单引号的标志位，初始值为false
        single_quotes_for_str = False
        # 创建指示双引号的标志位，初始值为false
        double_quotes = False
        # 创建指示字符串双引号的标志位，初始值为false
        double_quotes_for_str = False
        # 创建指示位于引号状态
        quotes = False
        # 指示当前字典的key
        key = None
        # 指示当前字典的value
        value = None
        # 指示是否遇到冒号
        colon = False
        # 指示上一个字符是否是反斜杠
        backslash = False
        for e in list(express):
            if e == "(" and parenthesis <= 0 and bracket <= 0:
                if not ParamType.is_method_name(value):
                    is_tuple = True
                    parenthesis_for_tuple += 1
            if e in ["\n", "\t", " "] and not quotes and bracket <= 0 and not is_tuple:
                continue
            if e == '{' and not quotes and bracket <= 0 and not is_tuple:
                cursor = {}
                stack.append({"key": key, "value": cursor})
                colon = False
            elif not colon and not single_quotes and e == '"' and bracket <= 0 and not is_tuple:
                double_quotes = not double_quotes
                quotes = double_quotes
                if double_quotes:
                    if not colon:
                        key = ""
            elif not colon and not double_quotes and e == "'" and bracket <= 0 and not is_tuple:
                single_quotes = not single_quotes
                quotes = single_quotes
                if single_quotes:
                    if not colon:
                        key = ""
            elif e == ":" and not quotes and bracket <= 0:
                colon = True
                value = ""
            elif e in [",", "}"] and parenthesis <= 0 and not quotes and bracket <= 0 and not is_tuple:
                colon = False
                if key is not None and value is not None:
                    # 对value进行计算
                    ex_o = Express(value)
                    r = ex_o.calculate(*context)
                    if r == Utils.ERROR:
                        raise Exception("其中的子表达式错误，错误原因:{}".format(ex_o.error))
                    value = r
                    cursor[key] = value
                key = None
                value = None
                if e == "}":
                    current = stack.pop()
                    k = current.get("key")
                    if k is not None:
                        parent = stack.pop()
                        parent_value = parent.get("value")
                        parent_value[k] = cursor
                        cursor = parent_value
                        stack.append(parent)
                    else:
                        return cursor
            elif e == "\\" and not backslash and bracket <= 0 and not is_tuple:
                backslash = True
            elif colon:
                if e == "'" and not backslash and not double_quotes_for_str:
                    single_quotes_for_str = not single_quotes_for_str
                    quotes = single_quotes_for_str
                if e == '"' and not backslash and not single_quotes_for_str:
                    double_quotes_for_str = not double_quotes_for_str
                    quotes = double_quotes_for_str
                if e == "(" and not backslash and not quotes and bracket <= 0 and not is_tuple:
                    parenthesis += 1
                if e == ")" and not backslash and not quotes and bracket <= 0 and not is_tuple:
                    parenthesis -= 1
                if e == "[" and not backslash and not quotes and not is_tuple:
                    bracket += 1
                if e == "]" and not backslash and not quotes and not is_tuple:
                    bracket -= 1
                if e == ")" and is_tuple and bracket <= 0 and not quotes and not backslash:
                    parenthesis_for_tuple -= 1
                    if parenthesis_for_tuple <= 0:
                        is_tuple = False
                backslash = False
                value += e
            else:
                if not (single_quotes or double_quotes):
                    raise Exception("单引号或双引号出错！")
                key += e
        r = stack.pop()
        if r.get("key") is not None:
            raise Exception("key出错！")
        return r.get("value")

    def __calculate_normal(self, *context):
        """
        计算普通表达式
        """
        # 得到表达式的每个操作数和运算符
        self.__process_to_express()
        # 遍历操作数和运算符，处理需要合并的运算符
        self.__process_in_ex()
        # 中缀转为后缀表达式
        self.__in_ex_to_post_ex()
        # 计算后缀表达式
        self.__calculate_post_ex(*context)
        return self.__re

    def __process_in_ex(self):
        """
        遍历操作数和运算符，处理需要合并的运算符和拆分运算数
        :return:
        """
        in_expression = self.__in_express
        new_in_expression = list()
        last = None
        for _in in in_expression:
            if last == "not" and _in == "in":
                new_in_expression.pop()
                new_in_expression.append("not in")
            elif ParamType.is_method(_in):
                name, params = ParamType.get_method_name_and_params_str(_in)
                if last == ".":
                    new_in_expression.append("-{}".format(name))
                else:
                    new_in_expression.append("+{}".format(name))
                param = ""
                left = 0
                for t in list(params):
                    if t == "(":
                        left += 1
                        param += t
                    elif t == ")":
                        left -= 1
                        param += t
                        if left == 0:
                            new_in_expression.append("->")
                            new_in_expression.append("f{}".format(param))
                            param = ""
                    else:
                        param += t
            elif last == "." and ParamType.is_var(_in):
                new_in_expression.append("-{}".format(_in))
            else:
                new_in_expression.append(_in)
            last = _in
        self.__in_express = new_in_expression

    @staticmethod
    def __only_float_to_decimal(f):
        """
        仅把float转decimal
        :param f:
        :return:
        """
        if type(f) is float:
            return Decimal(str(f))
        return f

    @staticmethod
    def __only_decimal_to_float(d):
        """
        仅把decimal转float
        :param d:
        :return:
        """
        if type(d) is Decimal:
            return float(d)
        return d

    @classmethod
    def __get_expression(cls, text):
        """
        从text里提取表达式，并返回一个字典
        :param text:
        :return:
        """
        express_l = list(text)
        dollar_sign = False
        expression_sign = False
        left_bracket = 0
        expression_l = []
        t_stack = []
        for e in express_l:
            if expression_sign:
                if e == "{":
                    # 说明在表达式里遇到了一个左括号，对这个左括号进行计数
                    left_bracket += 1
                if e == "}":
                    # 如果左括号数目大于0，说明这是表达式里的括号
                    if left_bracket > 0:
                        left_bracket -= 1
                    else:
                        # 如果左括号数目小于0，说明这是表达式结束的标志
                        dollar_sign = False
                        expression_sign = False
                        # 将堆栈区拼接成表达式
                        expression_l.append("".join(t_stack))
                        # 清空堆栈
                        t_stack.clear()
                        continue
                t_stack.append(e)
                continue
            if e == "{" and dollar_sign is True:
                # 说明一个表达式开始了
                expression_sign = True
                continue
            if e != "{" and dollar_sign is True:
                # 说明并不是表达式
                dollar_sign = False
                continue
            if e == "$":
                # 如果下一个字符是“{”则说明一个表达式开始了
                dollar_sign = True
        return expression_l

    @classmethod
    def get_express_list(cls, text):
        """
        从text里提取表达式
        :param text:
        :return:
        """
        return cls.__get_expression(text)

    @classmethod
    def get_var_for_sql(cls, var, default: bool):
        if (type(var) in [int, float]):
            return str(var)
        elif (type(var) == bool):
            return '1' if var == True else '0'
        else:
            if default:
                return "'{}'".format(str(var))
            else:
                return str(var)

    @classmethod
    def is_express(cls, express):
        """
        判断是否是express
        :param express:
        :return:
        """
        if len(express) >= 3:
            if express[0] == "$":
                if express[1] == "{":
                    if express[-1] == "}":
                        return True
        return False

    @classmethod
    def __is_special_express(cls, ex, symbol):
        """
        是symbol说明的式子吗？
        :param ex:
        :param symbol:
        :return:
        """
        if symbol == list:
            left = "["
            right = "]"
        elif symbol == dict:
            left = "{"
            right = "}"
        elif symbol == tuple:
            left = "("
            right = ")"
        else:
            raise Exception("传入错误的标志！")
        if ex[0] != left or ex[-1] != right:
            return False
        count = 0
        blacflash = False
        que = False
        single_que = False
        double_que = False
        for e in list(ex[:-1]):
            if e == "\\":
                blacflash = True
                continue
            if e == "'":
                single_que = not single_que
                que = single_que
            if e == '"':
                double_que = not double_que
                que = double_que
            if e == left and not blacflash and not que:
                count += 1
            elif e == right and not blacflash and not que:
                count -= 1
                if count == 0:
                    return False
            blacflash = False
        return True

    def calculate(self, *context):
        """
        约定如果返回错误标志则说明此表达式有误，当返回错误标志时，可以通过访问error获取具体的错误信息
        :param context:
        :return:
        """
        try:
            if self.__express_str == "":
                return ""
            # 判断表达式是否是字典
            express = self.__express_str.strip()
            if Express.__is_special_express(express, dict):
                return self.__calculate_dict(*context)
            elif Express.__is_special_express(express, list):
                return self.__calculate_list(*context)
            elif Express.__is_special_express(express, tuple):
                return self.__calculate_tuple(*context)
            else:
                return self.__calculate_normal(*context)
        except Exception as e:
            self.__error = "表达式 {} 错误，错误原因->{} ".format(self.__express_str, str(e))
            return Utils.ERROR

    @classmethod
    def calculate_in_config(cls, text, *context):
        """
        对text字符串进行计算，返回计算后的结果
        :param text:
        :param context:
        :return:
        """
        # ${1+3+3}abc
        # 提取${}中的序列
        text_copy = text
        m = Express.__get_expression(str(text))
        # 判断存在多少个表达式
        if len(m) == 1 and "${{{}}}".format(m[0]) == text:
            # 存在1个表达式，且表达式就等于text，将直接返回计算后的结果
            ex_o = Express(m[0])
            express_r = ex_o.calculate(*context)
            if express_r == Utils.ERROR:
                raise MyException(" {} 中的表达式计算错误，原因为:{}".format(text_copy, ex_o.error))
            else:
                text = express_r
        else:
            for o in m:
                from ...printer.debug_printer_ import DebugPrinter
                DebugPrinter.print_log("将执行表达式 ${{{}}}".format(o))
                ex_o = Express(o)
                express_r = ex_o.calculate(*context)
                DebugPrinter.print_log("表达式 ${{{}}} 已执行，其运算结果为 {}".format(o, express_r))
                if express_r == Utils.ERROR:
                    raise MyException(" {} 中的表达式计算错误，原因为：{}".format(text_copy, ex_o.error))
                else:
                    old = "${{{}}}".format(o)
                    text = text.replace(old, str(express_r))
        return text

    @classmethod
    def calculate_sql(cls, text, *context):
        """
        对text字符串进行计算，返回计算后的结果
        :param text:
        :param context:
        :return:
        """
        # ${1+3+3}abc
        # 提取${}中的序列
        from ..cfg.config import config
        text_copy = text
        m = Express.__get_expression(str(text))
        # 判断存在多少个表达式
        if len(m) == 1 and "${{{}}}".format(m[0]) == text:
            # 存在1个表达式，且表达式就等于text，将直接返回计算后的结果
            from ...printer.debug_printer_ import DebugPrinter
            DebugPrinter.print_log("将执行表达式 ${{{}}}".format(m[0]))
            ex_o = Express(m[0])
            express_r = ex_o.calculate(*context, inner(), outer(), config.vars, config.configs)
            if express_r == Utils.ERROR:
                raise MyException(" {} 中的表达式计算错误，原因为:{}".format(text_copy, ex_o.error))
            else:
                text = express_r
            DebugPrinter.print_log("表达式 ${{{}}} 已执行，其运算结果为 {}".format(m[0], express_r))
        else:
            for o in m:
                from ...printer.debug_printer_ import DebugPrinter
                DebugPrinter.print_log("将执行表达式 ${{{}}}".format(o))
                ex_o = Express(o)
                express_r = ex_o.calculate(*context, inner(), outer(), config.vars, config.configs)
                if express_r == Utils.ERROR:
                    raise MyException(" {} 中的表达式计算错误，原因为:{}".format(text_copy, ex_o.error))
                else:
                    old = "${{{}}}".format(o)
                    start = text.find(old)
                    default = True
                    if start > 0 and text[start - 1] == "'":
                        default = False
                    text = text.replace(old, cls.get_var_for_sql(express_r, default))
                DebugPrinter.print_log("表达式 ${{{}}} 已执行，其运算结果为 {}".format(o, express_r))
        return text

    @classmethod
    def calculate_str(cls, text, *context):
        """
        对text字符串进行计算，返回计算后的结果
        :param text:
        :param context:
        :return:
        """
        # ${1+3+3}abc
        # 提取${}中的序列
        from ..cfg.config import config
        text_copy = text
        m = Express.__get_expression(str(text))
        # 判断存在多少个表达式
        if len(m) == 1 and "${{{}}}".format(m[0]) == text:
            # 存在1个表达式，且表达式就等于text，将直接返回计算后的结果
            from ...printer.debug_printer_ import DebugPrinter
            DebugPrinter.print_log("将执行表达式 ${{{}}}".format(m[0]))
            ex_o = Express(m[0])
            express_r = ex_o.calculate(*context, outer(), inner(), config.vars, config.configs)
            if express_r == Utils.ERROR:
                raise MyException(" {} 中的表达式计算错误，原因为:{}".format(text_copy, ex_o.error))
            else:
                text = express_r
            DebugPrinter.print_log("表达式 ${{{}}} 已执行，其运算结果为 {}".format(m[0], express_r))
        else:
            for o in m:
                from ...printer.debug_printer_ import DebugPrinter
                DebugPrinter.print_log("将执行表达式 ${{{}}}".format(o))
                ex_o = Express(o)
                express_r = ex_o.calculate(*context, outer(), inner(), config.vars, config.configs)
                if express_r == Utils.ERROR:
                    raise MyException(" {} 中的表达式计算错误，原因为：{}".format(text_copy, ex_o.error))
                else:
                    old = "${{{}}}".format(o)
                    text = text.replace(old, str(express_r))
                DebugPrinter.print_log("表达式 ${{{}}} 已执行，其运算结果为 {}".format(o, express_r))
        return text
