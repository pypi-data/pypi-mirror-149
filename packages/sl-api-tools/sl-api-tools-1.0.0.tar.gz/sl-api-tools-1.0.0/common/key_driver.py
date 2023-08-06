# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : key_driver.py
# Time       ：2022-04-17 14:09
# Author     ：xuepl
# version    ：python 3.7.1
"""
import json
import re

import allure

from common.key_map import key_maps
from tools import log


class KeyDriver():

    def __init__(self, send_request, value):
        self.send_request = send_request
        self.value = self.to_str(value)
        self.key_replace()

    # 使用json.dumps 把字典或者list类型的数据，转换成字符串

    def to_str(self, value):  # 把所有类型的数据，转换为字符串类型
        if isinstance(value, dict) or isinstance(value, list):
            value = json.dumps(value, ensure_ascii=False)
        else:
            value = str(value)
        return value

    def keys_parser(self, value):
        '''
        返回字符串中所有的关键字
        $__PHONE()$
        $__RANDOM_STR(abceefg,10)$
        $__RANDOM_INT(6,18)$
        $__RANDOM_STR(abceefg,$__RANDOM_INT(6,18)$)$
        参数中包含特殊符号 $ ,
        一个字符串中，可能会包含多个关键字
        :return:
        '''
        length = len(value)  # 获取数据的长度
        start = -1  # 关键字的起始位置，-1 表示没有遇到关键字起始位置
        split_flag = 0  # 解决关键字多层嵌套，定义一个标记。为0表示关键字开始和结束是成对的
        __keys = []  # 关键字列表
        for i in range(length):  # for循环遍历整个字符串
            if (value[i] == "$"):
                # 关键字的起始字符
                if i + 2 < length and value[i:i + 3] == "$__":
                    split_flag -= 1  # 遇到关键字开始字符，split_flag值减一
                    if start < 0:  # 如果已经对关键字起始标志赋值完成，则不需要重复赋值
                        start = i
                # 关键字的结束字符
                elif i - 1 >= 0 and value[i - 1:i + 1] == ")$":
                    split_flag += 1  # 遇到关键字结束字符，split_flag值加一
                    if split_flag == 0:  # 遇到关键字结束字符，如果split_flag为0，则表示关键字完整结束，可以进行切片
                        __keys.append(value[start: i + 1])  # 关键字切片并存入列表中
                        start = -1  # 重置关键字开始标记
        return __keys

    def key_run(self, key):
        # 判断是否存在关键字嵌套
        if "$__" in key[3:-1]:
            # 获取关键字中的内层关键字
            inner_kyes = self.keys_parser(key[3:-1])
            # 循环执行所有的内层关键字
            for i_key in inner_kyes:
                res = self.key_run(i_key)  # 递归执行所有的内层关键字
                key = key.replace(i_key, res)  # 替换关键字中的内层关键字
        key_name = key[3:key.find('(')]  # 获取关键字名称
        r = re.compile(r"\((.*)\)")  # 此处不可以使用非贪婪模式
        key_args = r.findall(key)[0]  # 获取关键字参数
        res = None
        try:
            if key_args == "":  # 如果关键字参数为空
                res = key_maps[key_name](self.send_request)
            else:  # 如果关键字参数不为空
                res = key_maps[key_name](self.send_request, *key_args.split(','))  # *python中的解包赋值
        except AssertionError as e:
            raise
        except:
            log.error(f"关键字：{key}执行失败")
        return self.to_str(res) if res else None  # 把关键字执行结果转换为字符串

    def key_replace(self):
        # 解析数据中所有的关键字
        keys = self.keys_parser(self.value)
        # 把执行的关键字列表，添加进allure报告中
        allure.attach(json.dumps(keys, ensure_ascii=False, indent=2), "关键字列表",
                      attachment_type=allure.attachment_type.TEXT)
        for key in keys:
            # 循环执行关键字
            res = self.key_run(key)
            if res:
                self.value = self.value.replace(key, res)
        return self.value

    def __str__(self):
        # 重写__str__方法，返回value
        return self.value


if __name__ == '__main__':
    s = "adf$__RANDOM_STRING(1234567890,10)$f $__RANDOM_STRING(abceefg,$__RANDOM_INT(6,18)$)$"

    print(KeyDriver(s))
