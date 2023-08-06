# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : config.py
# Time       ：2022-03-27 17:29
# Author     ：xuepl
# version    ：python 3.7.1
"""
import configparser

# 创建一个初始化器
import os

from tools import log

config = configparser.ConfigParser()

# 获取配置文件的绝对路径
config_path = os.path.join(os.getcwd(), "config.ini")
# 读取配置文件
config.read(config_path, encoding='utf-8')


class Config():
    def __init__(self):
        # 获取环境号
        self.env = os.environ.get("AUTO_ENV")
        # self.env = "te"

    def get_url(self, app_name):
        section = self.env + "_url"
        return self.get_option(section, app_name)

    def get_db(self, app_name):
        # 拼接section
        section = f"{self.env}_{app_name}_db"
        # 根据section获取所有的option
        options = config.options(section)
        # res = {}
        # for o in options:
        #     res[o] = self.get_option(section, o)
        res = {o: self.get_option(section, o) for o in options}  # 字典推导式，根据options获取对应的value，并存入字典中
        res["port"] = int(res["port"])  # 把字符串格式的端口号，强转成数字格式
        return res

    def section_is_exist(self, section):
        return section in config.sections()  # 判断section是否存在

    def get_option(self, section, option):
        try:
            return config.get(section, option)
        except:
            assert False, f"配置文件中获取不到对应的记录,section: {section}, option：{option}"

    def get_root_path(self):
        root_path = self.get_option("root_path", "path")
        if root_path == "":
            root_path = os.path.dirname(config_path)
        return root_path
