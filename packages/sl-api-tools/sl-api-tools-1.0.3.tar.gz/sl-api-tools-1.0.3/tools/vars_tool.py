# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : vars_tool.py
# Time       ：2022-04-23 11:14
# Author     ：xuepl
# version    ：python 3.7.1
"""
import jsonpath

from tools import log
from tools.Tripartite_tool import MySQLTool


def db(send_request, app, var_name, *sql):
    """
    执行sql语句，如果是查询语句，并把执行结果存入local_vars字典中,如果是增删改语句，则不会存储执行结果
    :param send_request:
    :param app: 应用名
    :param var_name: 变量名
    :param sql: sql语句
    :return:
    """
    # 1、数据库连接信息
    db_config = send_request.request.config.get_db(app)
    db = MySQLTool(**db_config)
    sql = ",".join(sql)
    sql = sql.strip()  # 去掉前后空格
    if sql[:6].upper() == "SELECT":
        res = db.query(sql)
        log.debug(f"数据库查询成功，变量名为：{var_name} 变量值为：{res}")
        send_request.local_vars[var_name] = res
    else:
        res = db.update(sql)
        log.debug(f"数据库修改成功，影响行数为：{res}")


def get_var(send_request, var_name):
    """
    根据变量名，从字典send_request.local_vars中获取对应的数据
    :param send_request: SendRequest对象
    :param var_name: 变量名
    :return:
    """
    vars = send_request.local_vars
    if not var_name.startswith("$"):
        var_name = "$." + var_name
        var_name = var_name.replace('"', "'")
    res = jsonpath.jsonpath(vars, var_name)
    if res:
        return res[0]


def set_var(send_request, var_name, value):
    """
    把数据存入send_request.local_var 字典中
    :param send_request:
    :param var_name:  变量名
    :param value:  变量值
    :return:
    """
    send_request.local_vars[var_name] = value


'''
$.userInfo[0]['login_name']
$.token
local_vars = {
"token":"asdfsafasdf",
"userInfo":[{'login_name': '134', 'password_md5': ''}, {'login_name': '13818316417', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13818316418', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '18282101811', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '13873286446', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13222105193', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13240919655', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '15524407288', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '18023601866', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '15584015624', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '18635797377', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '15336801286', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13371762946', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '15927596993', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '15038517306', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '18195013465', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13438643969', 'password_md5': '96e79218965eb72c92a549dd5a330112'}, {'login_name': '13781670839', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '18260154769', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '14735489575', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '18077177958', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '15388781833', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '15983829075', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '13353770722', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '13353770744', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}, {'login_name': '13353770755', 'password_md5': 'e10adc3949ba59abbe56e057f20f883e'}]

}
'''


# 封装关键字，从config.ini文件中获取数据

def get_config(send_request, section, option):
    """
    获取config.ini中的数据
    :param send_request:
    :param section:
    :param option:
    :return:
    """
    return send_request.request.config.get_option(section, option)
