# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : key_map.py
# Time       ：2022-04-17 15:12
# Author     ：xuepl
# version    ：python 3.7.1
"""
from tools.data_tools import random_str, random_int, random_phone
from tools.post_process_tool import json_excutor, regex_excutor, assert_contains, assert_json_equals, assert_batch
from tools.vars_tool import get_var, db, set_var, get_config

key_maps = {
    "RANDOM_STRING": random_str,  # $__RANDOM_STRING(字符取值范围,长度)$ 示例： $__RANDOM_STRING(abcdefg,6)$
    "RANDOM_INT": random_int,  # $__RANDOM_INT(起始,结束)$ 示例： $__RANDOM_INT(6,18)$
    "PHONE": random_phone,  # $__PHONE()$ 示例： $__PHONE()$
    "JSON_EXCUTOR": json_excutor,
    # $__JSON_EXCUTOR(变量名,最终结果中的第几个小于1表示随机大于等于1表示第几个,jsonpath表达式)$ 示例： $__JSON_EXCUTOR(token,0,$.data)$
    "GET_VAR": get_var,  # $__GET_VAR(变量名)$ 示例： $__GET_VAR(变量名)$
    "SET_VAR": set_var,  # $__SET_VAR(变量名,变量值)$ 示例： $__SET_VAR(app,sdfadf)$
    "REGEX_EXCUTOR": regex_excutor,
    # $__REGEX_EXCUTOR(变量名,最终结果中的第几个小于1表示随机大于等于1表示第几个,正则表达式)$ 示例： $__REGEX_EXCUTOR(token,0,"data":"(.*?)")$
    "DB": db,
    # $__DB(应用名,变量名,sql语句)$ 示例： $__DB(mall,userInfo,SELECT login_name,password_md5 FROM `tb_newbee_mall_user`;)$
    "GET_CONFIG": get_config,  # $__GET_CONFIG(section,option)$ 示例： $__GET_CONFIG(user_info,login_name)$
    "ASSERT_CONTAINS": assert_contains,  # $__ASSERT_CONTAINS(预期结果)$  示例： $__ASSERT_CONTAINS("resultCode":200)$
    "ASSERT_JSON_EQUALS": assert_json_equals,
    # $__ASSERT_JSON_EQUAL(预期结果,jsonpath表达式)$  示例： $__ASSERT_JSON_EQUAL(200,$.resultCode)$
    "ASSERT_BATCH": assert_batch,
    # 批量断言$__ASSERT_BATCH(预期结果json字符串)$ 示例：$__ASSERT_BATCH({"resultCode":200,"message":"SUCCESS"})$

}
