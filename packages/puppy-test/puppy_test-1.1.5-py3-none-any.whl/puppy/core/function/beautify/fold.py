# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: fold text
"""
from ..cfg.config import config


class Fold(object):
    __fold_flag = "|-"
    __fold_text = config.get_config("fold_text", bool)
    __fold_text_when_more_than_lines = config.get_config("fold_text_when_more_than_lines", int)

    @classmethod
    def fold_text(cls, text):
        if cls.__fold_text is False:
            return text
        if text is None:
            return None
        old_text = str(text)
        if old_text.count("\n") <= cls.__fold_text_when_more_than_lines:
            return text
        new_text = ""
        count=0
        for _i in text.split("\n"):
            if count<cls.__fold_text_when_more_than_lines:
                count+=1
                new_text+="{}{}".format(_i,"\n")
            else:
                new_text += "{}{}{}".format(cls.__fold_flag, _i,"\n")
        return new_text
