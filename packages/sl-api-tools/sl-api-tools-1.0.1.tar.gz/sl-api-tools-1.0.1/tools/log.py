# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : log.py
# Time       ：2021/4/7 17:42
# Author     ：xuepl
# version    ：python 3.7
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler

'''
封装log方法
'''
logger = logging.getLogger(__name__)  # 获取日志记录器
logger.setLevel(level=logging.DEBUG)  # 设置日志记录器收集日志的最低级别DEBUG

root_path = os.path.join(os.getcwd(), "logs/")  # 确定日志输出的文件夹
if not os.path.exists(root_path):  # 如果log文件夹不存在，就去创建一个
    os.makedirs(root_path)
# 创建文件handler，
handler = TimedRotatingFileHandler(root_path + 'debug.log', when='d', interval=1, backupCount=30, encoding='utf-8')
handler.setLevel(logging.DEBUG)  # 设置该handler输出日志的最低级别为DEBUG
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # 日志格式化器，规定日志输出的格式
handler.setFormatter(formatter)
logger.addHandler(handler)

handler2 = TimedRotatingFileHandler(root_path + 'error.log', when='d', interval=1, backupCount=30, encoding='utf-8')
handler2.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler2.setFormatter(formatter)
logger.addHandler(handler2)

# handler 控制日志输出到控制台
handler3 = logging.StreamHandler()
handler3.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler3.setFormatter(formatter)
logger.addHandler(handler3)


def info(msg):
    logger.info(msg)


def debug(msg):
    logger.debug(msg)


def warning(msg):
    logger.warning(msg)


def error(msg):
    logger.error(msg)


def critical(msg):
    logger.critical(msg)
