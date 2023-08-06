import puppy
import shutil
import os
import unittest
# 取到puppy的static目录
puppy_path = puppy.__path__[0]
static_path = os.path.join(puppy_path, "static")
# 取到unittest的目录
unittest_path = unittest.__path__[0]
# 替换默认的main.py
# 先备份
src_main_file = os.path.join(static_path, "main.py")
main_file = os.path.join(unittest_path, "main.py")
new_main_file = os.path.join(unittest_path, "main.py.backup")
if os.path.exists(new_main_file):
    os.remove(new_main_file)
if os.path.exists(main_file):
    shutil.copy(main_file, new_main_file)
    os.remove(main_file)
shutil.copy(src_main_file, main_file)
print("已完成main.py文件替换")
