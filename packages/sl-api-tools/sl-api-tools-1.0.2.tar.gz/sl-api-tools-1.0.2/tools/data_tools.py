# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : data_tools.py
# Time       ：2022-04-17 15:13
# Author     ：xuepl
# version    ：python 3.7.1
"""
from faker import Faker
import random

fake = Faker("zh_CN")  # 默认英文，初始化为中文


def random_str(send_request, content, length):
    return "".join(random.choices(content, k=int(length)))


def random_int(send_request, start, end):
    return random.randint(int(start), int(end))


def random_phone(send_request):
    return fake.phone_number()


def random_idcard(send_request):
    # 随机身份证号
    pass
