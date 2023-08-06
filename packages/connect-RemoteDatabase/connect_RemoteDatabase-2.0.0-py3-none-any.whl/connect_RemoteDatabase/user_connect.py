#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# python 3.6
# @Project : connect
# @File    : user_connect.py
# @Date    : 2022/4/27 15:42
import pymysql

def create_conn(host, port, user, password, db, charset):
    # 创建连接
    conn = pymysql.connect(
        host=host,
        port=port,  # MySQL的默认端口
        user=user,  # 用户名
        password=password,  # 密码
        db=db,  # 用到的数据库
        charset=charset,
        autocommit=True
    )
    return conn
