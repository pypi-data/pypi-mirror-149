# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : base_request_des.py
# Time       ：2022-04-17 10:36
# Author     ：xuepl
# version    ：python 3.7.1
"""

# !/usr/bin/env python
# -*-coding:utf-8 -*-
from common.descrip import UrlDesc, ParamsDesc, JsonDesc, HeadersDesc, FilesDesc, ConfigDesc, MethodDesc

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

class BaseRequest():
    url = UrlDesc()
    app = None
    method = MethodDesc()
    params = ParamsDesc()
    data = JsonDesc()
    json = JsonDesc()
    headers = HeadersDesc()
    files = FilesDesc()
    config = ConfigDesc()
