# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : response_tool.py
# Time       ：2022-04-23 9:39
# Author     ：xuepl
# version    ：python 3.7.1
"""
import json
import random
import re

import allure

from tools import log

'''
响应数据的提取

根据关键字，从响应中提取内容
提取方法：json表达式，正则表达式
响应数据的传递问题

下个接口中，怎么去获取提取出的数据
类变量做一个全局的数据变量
在定义一个从类变量中获取数据的关键字

$      代表json数据根节点
.或[]  获取对象中的节点  $['data'] 或 $.data
?()    跟判断条件  $.data.list[?(@.goodsName=='蔡徐坤')].goodsId
@      代表当前节点
[]     数据的迭代标识   $.data.list[0].goodsId
...    表示获取json中所有的节点  $...goodsId
[,]    支持迭代器中多选    $.data.list[0,1]['goodsId']
()     支持数据计算       $.data.list[(@.length-2)]['goodsId']
*      通配符代表任意字符       $.data.list[*].goodsId

python中，对jsonpath进行解析的模块叫做jsonpath
pip install jsonpath

使用
jsonpath.jsonpath(python字典或列表,json表达式)
返回值 jsonpath表达式不正确返回，False，匹配到数据返回列表
'''
import jsonpath


#
# d = {
#     "name": "王大锤",
#     "age": "12",
#     "sex": "男",
#     "addr": "上海闵行",
# }
# print(jsonpath.jsonpath(d, '$["name"]'))


def json_excutor(send_request, var_name, index, *json_path):
    """

    :param send_request:
    :param var_name: 变量名
    :param index: <=0 表示随机，如果为1 表示获取第1个数据，为2获取第二个数据依次类推
    :param *json_path: jsonpath表达式
    :return:
    """
    # 先判断send_request对象中，是否有response属性
    json_path = ','.join(json_path)  # 把元组转换为字符串
    if not hasattr(send_request, "response"):
        log.error(f"$__JSON_EXCUTOR({index},{json_path})$关键字，只能用于post_process或者assert中")
        return
    response = None
    # 获取并判断相应正文中数据是否是json格式
    try:
        response = send_request.response.response_body_dict
    except:
        log.error(f"$__JSON_EXCUTOR({index},{json_path})$关键字，只能用于响应数据为json格式的")
        return
    json_path = json_path.replace('"', "'")
    res_list = jsonpath.jsonpath(response, json_path)
    if res_list:
        index = int(index)
        if index > 0:
            res = res_list[index - 1]
        else:
            res = random.choice(res_list)
        send_request.local_vars[var_name] = res
        log.debug(f"json提取成功，变量: {var_name} 的值为: {res}")


def regex_excutor(send_request, var_name, index, *regex):
    """
    根据正则表达式提取响应中的数据，并存入变量var_name中。index值小于1 表示随机。等于1表示获取第一个结果
    :param send_request: SendRequest对象
    :param var_name: 变量名
    :param index: <=0 表示随机，如果为1 表示获取第1个数据，为2获取第二个数据依次类推
    :param regex: 正则表达式
    :return:
    """
    # 先判断send_request对象中，是否有response属性
    regex = ','.join(regex)  # 把元组转换为字符串
    if not hasattr(send_request, "response"):
        log.error(f"$__REGEX_EXCUTOR({index},{regex})$关键字，只能用于post_process或者assert中")
        return
    text = send_request.response.response_body_text
    try:
        r = re.compile(regex)
        res = r.findall(text)
        if not len(res) == 0:
            a = None
            index = int(index)
            if index < 1:
                a = random.choice(res)
            else:
                a = res[index - 1]
            log.debug(f"正则提取成功，变量: {var_name} 的值为: {a}")
            send_request.local_vars[var_name] = a
    except:
        log.error(f"正则表达式错误：{regex}")


# 断言

def assert_contains(send_request, *expect):
    """
    断言相应正文中是否包含预期结果
    :param send_request:
    :param expect:
    :return:
    """
    expect = ",".join(expect)
    if not hasattr(send_request, "response"):
        log.error(f"$__ASSERT_EXPECT({expect})$关键字，只能用于post_process或者assert中")
        raise
    try:
        assert expect in send_request.response.response_body_text
    except:
        log.error(f"断言失败：响应正文中不包含：{expect}")
        raise
    else:
        log.info(f"断言通过：响应正文中包含：{expect}")


def assert_json_equals(send_request, expect, *json_path):
    """
    断言json_path表达式对应的数据，和预期结果相等
    :param send_request:
    :param expect:
    :param json_path:
    :return:
    """
    # 先判断send_request对象中，是否有response属性
    json_path = ','.join(json_path)  # 把元组转换为字符串
    if not hasattr(send_request, "response"):
        log.error(f"$__ASSERT_JSON({expect},{json_path})$关键字，只能用于post_process或者assert中")
        raise
    response = None

    # 获取并判断相应正文中数据是否是json格式
    try:
        response = send_request.response.response_body_dict
    except:
        log.error(f"$__ASSERT_JSON({expect},{json_path})$关键字，只能用于响应数据为json格式的")
        raise
    json_path = json_path.replace('"', "'")
    res = jsonpath.jsonpath(response, json_path)
    try:
        if res:
            assert str(res[0]) == expect, f"断言失败：jsonpath：{json_path} 对应的数据 {res[0]} 不等于预期结果： {expect}"
        else:
            with allure.step(f"关键字：$__ASSERT_JSON_EQUAL({expect},{json_path})$ 断言结果：不通过"):
                allure.attach(f"断言失败：jsonpath：{json_path} 对应的数据不存在", "断言详情",
                              attachment_type=allure.attachment_type.TEXT)
            assert False, f"断言失败：jsonpath：{json_path} 对应的数据不存在"
    except Exception as e:
        with allure.step(f"关键字：$__ASSERT_JSON_EQUAL({expect},{json_path})$ 断言结果：不通过"):
            allure.attach(f"实际结果：{str(res[0])}  预期结果： {expect}", "断言详情",
                          attachment_type=allure.attachment_type.TEXT)
        log.error(e)
        raise
    else:
        with allure.step(f"关键字：$__ASSERT_JSON_EQUAL({expect},{json_path})$ 断言结果：通过"):
            allure.attach(f"实际结果：{str(res[0])}  预期结果： {expect}", "断言详情",
                          attachment_type=allure.attachment_type.TEXT)
        log.info(f"断言通过：jsonpath：{json_path} 对应的数据 {res[0]} 等于预期结果： {expect}")


def assert_batch(send_request, *expect):
    """
    批量断言
    :param send_request:
    :param *expect: 预期结果，json字符串
    :return:
    """
    expect = ','.join(expect)  # 把元组转换为字符串
    if not hasattr(send_request, "response"):
        log.error(f"$__ASSERT_JSON({expect})$关键字，只能用于post_process或者assert中")
        raise
    response = None
    # 获取并判断相应正文中数据是否是json格式
    try:
        response = send_request.response.response_body_dict
    except:
        log.error(f"$__ASSERT_JSON({expect})$关键字，只能用于响应数据为json格式的")
        raise
    try:
        expect = json.loads(expect)
    except:
        log.error(f"预期结果需要是一个json字符串: {expect}")
        raise

    def compare_json(response, expect):
        '''
        对比预期结果和响应数据
        :param response:
        :param expect:
        :return:
        '''
        if isinstance(expect, dict) and isinstance(response, dict):
            for k in expect:
                if k in response:
                    compare_json(response[k], expect[k])
        elif isinstance(expect, list) and isinstance(response, list):
            for i in range(len(expect)):
                if i <= len(response):
                    compare_json(response[i], expect[i])
        elif isinstance(expect, type(response)):
            try:
                assert expect == response
            except:
                log.error(f"断言失败：实际结果：{response} 和预期结果：{expect} 不一致")
                raise
            else:
                log.info(f"断言通过：实际结果：{response} 和预期结果：{expect} 相等")
        else:
            log.error(f"断言失败：预期结果：{expect} 和实际结果：{response} 数据类型不一致")
            raise AssertionError("断言类型错误")

    compare_json(expect, response)
