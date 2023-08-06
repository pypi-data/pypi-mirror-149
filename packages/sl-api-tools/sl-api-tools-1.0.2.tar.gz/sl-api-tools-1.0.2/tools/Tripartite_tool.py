# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : mysql_tool.py
# Time       ：2022-04-23 14:16
# Author     ：xuepl
# version    ：python 3.7.1
"""

import pymysql


class MySQLTool():
    def __init__(self, host, user, password, db, port=3306, charset="utf8"):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port
        self.charset = charset

    def connect(self):
        # 建立数据库链接
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.db,
            port=self.port,
            charset=self.charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建游标
        self.cursor = self.conn.cursor()

    def query(self, sql):
        '''
        查询
        :param sql: sql语句
        :return:
        '''
        self.connect()
        self.cursor.execute(sql)  # 执行sql语句
        res = self.cursor.fetchall()  # 获取所有的查询结果
        self.close()
        return res

    def update(self, sql):
        '''
        增删改
        :param sql:sql语句
        :return:
        '''
        self.connect()
        effect_row = self.cursor.execute(sql)  # 执行sql语句
        self.conn.commit()  # 增删改必须要提交，不然不生效
        self.close()
        return effect_row

    def close(self):
        self.cursor.close()  # 关闭游标
        self.conn.close()  # 关闭数据库链接


if __name__ == '__main__':
    db = MySQLTool(host="api.xuepl.com.cn", user="root", password="SongLin2021", db="mall")
    res = db.query("SELECT * FROM `tb_newbee_mall_user`;")
    print(res)
    # 2022-04-23 14:23:20
