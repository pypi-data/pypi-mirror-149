# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_request.py
# Time       ：2022-04-10 10:52
# Author     ：xuepl
# version    ：python 3.7.1
"""

# 基础请求类

# 目的是给requests框架提供数据
# requests框架，在发送请求时，需要那些参数？
# url:str method:str params:dict data:dict或str json: dict headers:dict file:dict
import json
import os

from tools.config import Config
from tools.utils import kvstr_to_dict, hstr_to_dict


# 也可以定义成描述器的写法


class BaseRequest():
    __url = None
    app = None
    method = None
    __params = None
    __data = None
    __json = None
    __headers = None
    __files = None
    __config = None

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, value):
        try:
            self.__data = json.loads(value)
        except:
            self.__data = value

    @property
    def json(self):
        return self.__json

    @json.setter
    def json(self, value):
        try:
            self.__json = json.loads(value)
        except:
            self.__json = value

    @property
    def config(self):
        if self.__config is None:
            __class__.__config = Config()  # 避免后续用例中，多次实例化BaseRequest 类是，对Config类多次实例化
        return self.__config

    @property
    def url(self):  # 对url数据进行处理，返回完整的参数
        return self.config.get_url(self.app) + self.__url

    @url.setter
    def url(self, value):
        self.__url = value

    @property
    def params(self):  # 对prams数据返回时进行一个格式转换

        return self.__params

    @params.setter
    def params(self, value):
        # 对prams数据存储时进行一个格式转换
        if isinstance(value, dict):
            self.__params = value
        elif (isinstance(value, str)):
            self.__params = kvstr_to_dict(value)

    @property
    def files(self):  # 对prams数据返回时进行一个格式转换
        if not self.__files:
            return
        try:
            if isinstance(self.__files, str):
                self.__files = self.__files.replace("(", "[")
                self.__files = self.__files.replace(")", "]")
            self.__files = json.loads(self.__files)
        except:
            pass
        if isinstance(self.__files, dict):
            for k in self.__files:
                if isinstance(self.__files[k], str):
                    self.__files[k] = open(os.path.join(self.config.get_root_path(), self.__files[k]), 'rb')

        elif isinstance(self.__files, list) or isinstance(self.__files, tuple):
            '''
        [('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
        ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
        
        [('images',open('foo.png', 'rb')),
        ('images', open('bar.png', 'rb'))]
        '''
            self.__files = list(self.__files)  # 把元组类型数据，转换为列表类型
            for i in range(len(self.__files)):
                file = list(self.__files[i])
                if isinstance(file[1], str):
                    file[1] = open(os.path.join(self.config.get_root_path(), file[1]), 'rb')  # 二进制格式打开文件
                    self.__files[i] = tuple(file)
                elif isinstance(file[1], tuple) or isinstance(file[1], list):
                    file[1] = list(file[1])
                    file[1][1] = open(os.path.join(self.config.get_root_path(), file[1][1]), 'rb')
                    file[1][1] = tuple(file[1][1])
                    file[1] = tuple(file[1])

        return self.__files

    @files.setter
    def files(self, value):
        self.__files = value

    @property
    def headers(self):  # 对prams数据返回时进行一个格式转换
        return self.__headers

    @headers.setter
    def headers(self, value):
        if isinstance(value, dict):
            self.__headers = value
        elif isinstance(value, str):
            self.__headers = hstr_to_dict(value)
