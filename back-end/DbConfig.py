# -*- coding = utf-8 -*-
# -*- coding: gb2312 -*-
# @Time  : 2023/11/20 10:27
# @Author : 张听
# @File : DbConfig.py
# @Software: PyCharm
#数据库连接配置
import pymysql

conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        password='******',
        database='graduation_project'
    )
