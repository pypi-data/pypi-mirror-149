#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tools import os_tool
import os

############################
# 初始化工程目录
############################
root_path = os_tool.get_root_path()

content = """[te_url]
mall = http://api.xuepl.com.cn:28019
admin = http://api.xuepl.com.cn:27019
srb = http://srb.xuepl.com.cn:81
[re_url]
mall = http://1.15.183.200:28019
admin = http://1.15.183.200:27019


[te_mall_db]
host = api.xuepl.com.cn
user = root
password = SongLin2021
db = mall
port = 3306

[te_admin_db]
host = api.xuepl.com.cn
user = root
password = SongLin2021
db = mall
port = 3306

[re_mall_db]
host = 1.15.183.200
user = root
password = SongLinxy
db = mall
port = 3306

[re_admin_db]
host = 1.15.183.200
user = root
password = SongLinxy
db = mall
port = 3306

[root_path]
path = E:\\case



[user_info]
login_name = 13090237226
password = e10adc3949ba59abbe56e057f20f883e"""
os_tool.mkfile(root_path, *['./', 'config.ini'], content=content)

content = """# !/usr/bin/env python
# -*-coding:utf-8 -*-

'''
# File       : conftest.py.py
# Time       ：2022-03-27 17:01
# Author     ：xuepl
# version    ：python 3.7.1
'''

# 1、注册自定义命令行参数
import os

import pytest

from tools import log
from tools.utils import get_cases


def pytest_addoption(parser):
    parser.addoption("--env", action="store",  # append
                     default="te",
                     help="指定测试环境 te, re ,pe，默认为：te")


# 2、获取命令行参数的值
@pytest.fixture(scope="session", autouse=True)
def env(request):
    # 获取环境号
    envNo = request.config.getoption("--env")
    log.info(f"------------运行环境：{envNo}----------")
    if envNo not in ["te", "re", "pe"]:  # 判断获取到的环境号，是否存在于环境列表中
        pytest.exit("请输入正确的环境号！")  # 直接结束，不运行测试用例
    # 把环境号写入环境变量
    os.environ.setdefault("AUTO_ENV", envNo)


def pytest_collection_modifyitems(session, config, items) -> None:
    # item表示每个测试用例，解决用例名称中文显示问题
    for item in items:
        item.name = item.name.encode("utf-8").decode("unicode-escape")
        item._nodeid = item._nodeid.encode("utf-8").decode("unicode-escape")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # 获取钩子方法的调用结果
    out = yield
    # print('用例执行结果', out)
    # 从钩子方法的调用结果中获取测试报告
    report = out.get_result()
    # when 常见有三 setup call teardown
    # outcome 常见值有三  passed 通过  failed 执行失败的用例 skipped 跳过执行的用例（包括所有用装饰器标记的）
    # duration 用例的执行耗时
    # 执行时间，用例路径，用例执行结果。执行通过打印用例耗时。如何执行不通过，打印报错信息
    if report.when == "call":
        if report.outcome == 'failed':
            log.error(f"用例执行路径：{report.location[0]}::{report.location[2]},用例执行结果：{report.outcome}\\n{report.longrepr}")
        else:
            log.info(
                f"用例执行路径：{report.location[0]}::{report.location[2]},用例执行结果：{report.outcome},用例执行耗时为：{report.duration}")


# 使用钩子函数，实现自动参数化
def pytest_generate_tests(metafunc):
    ''' generate (multiple) parametrized calls to a test function.'''
    ids, cases = get_cases()
    if "case" in metafunc.fixturenames:
        metafunc.parametrize("case",
                             cases,
                             ids=ids,
                             scope="function")
"""
os_tool.mkfile(root_path, *['./', 'conftest.py'], content=content)

content = """# !/usr/bin/env python
# -*-coding:utf-8 -*-

'''
# File       : run.py
# Time       ：2022-05-08 11:28
# Author     ：xuepl
# version    ：python 3.7.1
'''
import os

import pytest

report_data = "report/json"
pytest.main(["--alluredir", report_data, '--env', 'te'])
"""
os_tool.mkfile(root_path, *['./', 'run.py'], content=content)

content = """# !/usr/bin/env python
# -*-coding:utf-8 -*-

'''
# File       : test_run.py
# Time       ：2022-05-08 11:27
# Author     ：xuepl
# version    ：python 3.7.1
'''
from common.send_request import SendRequest


def test_run(case):
    SendRequest(case).send()
"""
os_tool.mkfile(root_path, *['./', 'test_run.py'], content=content)
