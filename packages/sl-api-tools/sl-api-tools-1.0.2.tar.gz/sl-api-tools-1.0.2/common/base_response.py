# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_response.py
# Time       ：2022-04-10 16:35
# Author     ：xuepl
# version    ：python 3.7.1
"""
from tools import log
from tools.utils import hdict_to_str


class BaseResponse():
    def __init__(self, response):
        self.response = response
        self.__print_log()

    @property
    def status_code(self):
        return self.response.status_code

    @property
    def response_headers(self):
        return hdict_to_str(self.response.headers)

    @property
    def response_body_text(self):
        return self.response.text

    @property
    def response_body_dict(self):
        return self.response.json()

    @property
    def response_body_content(self):
        return self.response.content

    @property
    def request_method(self):
        return self.response.request.method

    @property
    def request_url(self):
        return self.response.request.url

    @property
    def request_headers(self):
        return hdict_to_str(self.response.request.headers)

    @property
    def request_body(self):
        return self.response.request.body if self.response.request.body else ""

    def __print_log(self):
        # 打印请求信息
        log.info(f"""
------------------请求报文-----------------
{self.request_method} {self.request_url}
{self.request_headers}

{self.request_body}""")
        # 打印响应信息
        log.info(f"""
---------响应报文-----------------
{self.status_code}
{self.response_headers}

{self.response_body_text}""")

    def __str__(self):
        return f"""
---------响应报文-----------------
{self.status_code}
{self.response_headers}

{self.response_body_text}"""
