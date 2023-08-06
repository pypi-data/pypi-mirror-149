# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : send_request.py
# Time       ：2022-04-10 14:13
# Author     ：xuepl
# version    ：python 3.7.1
"""
import json
import os

import allure
import requests

from common.base_request_des import BaseRequest
from common.base_response import BaseResponse
from common.key_driver import KeyDriver


class SendRequest():
    __session = None
    local_vars = {}

    def __init__(self, case):
        self.request = BaseRequest()  # 实例化BaseRequest对象
        self.request_data = {}
        self.request.url = (case["url"], case["app"])
        self.allure_data = {"feature": case["app"]}
        for key in case:  # 遍历dict 对BaseRequest对象 赋值
            if key in ["pre_process"]:
                self.pre_process = case["pre_process"]
            elif key in ["assert"]:
                self.assert_data = case["assert"]
            elif key in ["post_process"]:
                self.post_process = case["post_process"]
            elif key in ['app', 'method', 'params', 'data', 'json', 'headers', 'files']:
                self.request_data[key] = case[key]
            elif key in ["story", "title"]:
                self.allure_data[key] = case[key]
        # 添加allure报告数据
        for key in self.allure_data:
            getattr(allure.dynamic, key)(self.allure_data[key])

    # 扩展
    # 1、session发送
    # 2、请求头中的默认值

    @property
    def session(self):
        if self.__session is None:
            __class__.__session = requests.Session()
            self.__session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
            })
        return self.__session

    def send(self):
        # 第一步，执行前置操作
        with allure.step("第一步、执行前置操作"):
            KeyDriver(self, self.pre_process)  # 关键字驱动
        # 第二步，发送请求
        with allure.step("第二步、发送请求"):
            allure.attach(json.dumps(self.request_data, ensure_ascii=False, indent=2), "请求数据",
                          attachment_type=allure.attachment_type.TEXT)
            self.request_data = json.loads(str(KeyDriver(self, self.request_data)))  # 关键字驱动
            for key in self.request_data:
                setattr(self.request, key, self.request_data[key])  # 使用反射的方法，对request对象进行赋值
            # 发送请求
            r = self.session.request(
                method=self.request.method,
                url=self.request.url,
                params=self.request.params,
                data=self.request.data,
                json=self.request.json,
                headers=self.request.headers,
                files=self.request.files
            )
            # 初始化为响应数据类
            self.response = BaseResponse(r)
            # 添加请求和响应数据，至测试报告中
            allure.attach(str(self.response), "响应数据",
                          attachment_type=allure.attachment_type.TEXT)
        # 第三步，执行后置操作
        with allure.step("第三步，执行后置操作"):
            KeyDriver(self, self.post_process)  # 关键字驱动
        # 第四步、断言
        with allure.step("第四步、断言"):
            KeyDriver(self, self.assert_data)  # 关键字驱动
