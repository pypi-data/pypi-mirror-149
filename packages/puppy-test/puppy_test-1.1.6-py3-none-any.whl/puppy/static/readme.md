#### **项目介绍**
```
名称：puppy
描述：一个简单的API自动化测试框架，支持http和tcp协议，自动生成报告。
说明：
    1、支持无代码化脚本编写
    2、支持TCP和HTTP(s)协议
    3、支持数据库调用
    4、支持简易表达式
    5、支持简单的分支循环
    6、可自定义函数
插件说明：
    1：支持xml直接运行，无需再定位至对应py文件进行执行
    2：interface、casexml代码快速模板
    3：接口跳转
    4：参数提示
```
#### **使用说明**
```
一、安装第三方库
    1、requests==2.25.0
    2、PyMySQL==0.9.3（可选，如需操作mysql数据库必须）
    3、cx-Oracle==8.2.1（可选，如需操作oracle数据库必须）
    4、selenium==3.141.0（可选，如需操作selenium必须）
    5、JPype1==1.3.0（可选，如需操作jvm必须）
    
二、安装pycharm插件（可选）
    1、将file/plugins下的PuppyPlugin-x.x-SNAPSHOT.zip直接拖入到pycharm编辑窗口即可安装。
    2、将file/plugins下的main.py替换至python安装目录\Lib\unittest\main.py，替换后可支持在xml里执行单个用例。
    (3)、若插件未生效，点击[File]-[Settings]-[Plugins]-[Installed]-[勾选Puppy plugin!]-[ok]
    注：pycharm版本须为pycharm-professional-2020.2-2021.1版本

三、案例执行
    单个案例执行：
        1、安装了插件：直接在test_data目录下的案例xml上右键执行。
        2、未安装插件：执行test_case目录下的案例xml对应的py文件。
    批量执行：
        1、批量执行第一种方式：在pycharm直接执行runner.py，执行时控制台将不会打印日志，执行完成将输出报告。
        2、批量执行第二种方式：在命令提示符进入到项目目录，输入python runner.py进行执行，执行完成将输出报告。
```



