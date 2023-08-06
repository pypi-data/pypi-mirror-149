# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : utils.py
# Time       ：2022-04-10 11:26
# Author     ：xuepl
# version    ：python 3.7.1
"""
import json
import os

import xlrd

from tools import log
from tools.config import Config


def kvstr_to_dict(s):
    d = {}
    try:
        d = json.loads(s)
    except:
        pass
    else:
        return d
    if "=" not in s:
        log.error(f"参数必须是键值对类型: {s}")
        return d
    kvs_list = s.split("&")

    for kvs in kvs_list:
        k, v = kvs.split('=')
        d[k] = v
    return d


def hstr_to_dict(s):
    d = {}
    s = s.strip()  # 去调前后空格
    kvs_list = s.split('\n')
    try:
        d = json.loads(s)
    except:
        pass
    else:
        return d

    for kvs in kvs_list:
        kvs = kvs.strip()
        k, v = kvs.split(": ")
        d[k] = v
    return d


def hdict_to_str(d):
    h_list = []
    for k, v in d.items():
        h_list.append(f"{k}: {v}")
    return "\n".join(h_list)


def read_json_file(file_path):
    res = None
    with open(file_path, 'r', encoding='utf-8') as f:
        res = json.loads(f.read())
    return res


def read_excel(file_path):
    root_path = Config().get_root_path()
    # 打开excel文件
    excel = xlrd.open_workbook(os.path.join(root_path, file_path))
    # 获取excel中所有的sheet
    sheets = excel.sheets()
    case_lsit = []  # 用例数据列表
    ids = []
    for sheet in sheets:
        # 获取当前sheet中，总共有多少行数据
        rows = sheet.nrows
        if rows < 2:
            continue
        # 读取第一行数据
        row_1 = sheet.row_values(1)
        # 使用for循环，读取当前sheet中所有的行
        for i in range(2, rows):
            row = sheet.row_values(i)
            # 把每行内容转换成一个字典，字典的key是对应列第一行数据，值为对应列当前行数据
            d = {}
            for n in range(len(row)):
                d[row_1[n]] = None if row[n] == '' else row[n]
            if d["is_run"] and d["is_run"].strip() == '否':
                continue
            ids.append(d["title"])
            case_lsit.append(d)  # 用例数据放入case_list中
    return ids, case_lsit


def scan_excel(file_path, excel_list):
    files_list = os.listdir(file_path)
    for f in files_list:
        file = os.path.join(file_path, f)  # 路径拼接
        # 判断是否是一个文件夹
        if os.path.isdir(file) and f not in [".git", ".idea", '.pytest_cache', '__pycache__']:
            scan_excel(file, excel_list)
        elif os.path.isfile(file) and (file.endswith(".xls") or file.endswith(".xlsx")):  # 判断是excel文件
            excel_list.append(file)
            pass
        else:
            # 文件路径不存在
            pass


def get_cases():
    root_path = Config().get_root_path()
    excel_list = []
    # 递归结束之后，所有的excel文件路径已经存入excel_list中
    scan_excel(root_path, excel_list)
    # 批量读取excel文件中的数据，并存放至列表中
    ids = []
    cases = []
    for e in excel_list:
        titles, case_lsit = read_excel(e)
        ids.extend(titles)
        cases.extend(case_lsit)
    return ids, cases


if __name__ == '__main__':
    get_cases()
