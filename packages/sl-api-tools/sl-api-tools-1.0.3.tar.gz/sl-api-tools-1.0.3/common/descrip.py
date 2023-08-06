# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : descrip.py
# Time       ：2022-04-17 11:01
# Author     ：xuepl
# version    ：python 3.7.1
"""

import json
import os

from tools.config import Config
from tools.utils import kvstr_to_dict, hstr_to_dict


# 也可以定义成描述器的写法

# 描述器基类
class BaseDesc():
    __config = None

    @property
    def config(self):
        if self.__config is None:
            __class__.__config = Config()  # 避免后续用例中，多次实例化BaseRequest 类是，对Config类多次实例化
        return self.__config


class MethodDesc(BaseDesc):
    __value = None

    def __get__(self, instance, owner):
        return self.__value

    def __set__(self, instance, value):
        self.__value = value


class ConfigDesc(BaseDesc):

    def __set__(self, instance, value):
        pass

    def __get__(self, instance, owner):
        return self.config


class UrlDesc(BaseDesc):
    __value = None
    __app = None

    def __set__(self, instance, value):
        self.__value = value[0]
        self.__app = value[1]

    def __get__(self, instance, owner):
        return self.config.get_url(self.__app) + self.__value


class ParamsDesc(BaseDesc):
    __value = None

    def __set__(self, instance, value):
        # 对prams数据存储时进行一个格式转换
        if isinstance(value, dict):
            self.__value = value
        elif (isinstance(value, str)):
            self.__value = kvstr_to_dict(value)

    def __get__(self, instance, owner):
        return self.__value


class JsonDesc(BaseDesc):
    __value = None

    def __set__(self, instance, value):
        # 如果json字符串转为字典
        try:
            self.__value = json.loads(value)
        except:
            self.__value = value

    def __get__(self, instance, owner):
        return self.__value


class HeadersDesc(BaseDesc):
    __value = None

    def __set__(self, instance, value):
        # 如果json字符串转为字典,键值对字符串转为字典格式
        if isinstance(value, dict):
            self.__value = value
        elif isinstance(value, str):
            self.__value = hstr_to_dict(value)

    def __get__(self, instance, owner):
        return self.__value


class FilesDesc(BaseDesc):
    __value = None

    def __set__(self, instance, value):
        if not self.__value:
            return
        try:
            if isinstance(self.__value, str):
                self.__value = self.__value.replace("(", "[")
                self.__value = self.__value.replace(")", "]")
            self.__value = json.loads(self.__value)
        except:
            pass
        if isinstance(self.__value, dict):
            for k in self.__value:
                if isinstance(self.__value[k], str):
                    self.__value[k] = open(os.path.join(self.config.get_root_path(), self.__value[k]), 'rb')

        elif isinstance(self.__value, list) or isinstance(self.__value, tuple):
            '''
        [('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
        ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]

        [('images',open('foo.png', 'rb')),
        ('images', open('bar.png', 'rb'))]
        '''
            self.__value = list(self.__value)  # 把元组类型数据，转换为列表类型
            for i in range(len(self.__value)):
                file = list(self.__value[i])
                if isinstance(file[1], str):
                    file[1] = open(os.path.join(self.config.get_root_path(), file[1]), 'rb')  # 二进制格式打开文件
                    self.__value[i] = tuple(file)
                elif isinstance(file[1], tuple) or isinstance(file[1], list):
                    file[1] = list(file[1])
                    file[1][1] = open(os.path.join(self.config.get_root_path(), file[1][1]), 'rb')
                    file[1][1] = tuple(file[1][1])
                    file[1] = tuple(file[1])

        return self.__value

    def __get__(self, instance, owner):
        return self.__value
