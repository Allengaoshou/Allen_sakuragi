#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# import pymysql
# pymysql.install_as_MySQLdb()


# app = Flask(__name__)

# app.secret_key = 'some_secret'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/dutylist?charset=utf8'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/dutylist?charset=utf8'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_BINDS'] ={
#     "jimu":"mysql+pymysql://root:123123@172.16.3.173:3306/node_jimu_system?charset=utf8",
#     "ywcs":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/renrendai_0513?charset=utf8",
#     "marketing":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/marketing?charset=utf8",
#     "hxb":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.122:3306/renrendai_0513?charset=utf8"
# }
# db = SQLAlchemy(app)

SQLALCHEMY_TRACK_MODIFICATIONS = False
#session必须要设置key
SECRET_KEY='WWWWWWRRj/3yX R~XHH!jmN]LWX/,?RP'

#mysql数据库连接信息,这里改为自己的账号
# "uat":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.42:3306/renrendai_0513?charset=utf8",
# SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/BACKENDQA?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:1234@localhost:3306/dutylist?charset=utf8"
SQLALCHEMY_BINDS ={
    "jimu":"mysql+pymysql://root:123123@172.16.3.173:3306/node_jimu_system?charset=utf8",
    "ywcs":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/renrendai_0513?charset=utf8",
    "marketing":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/marketing?charset=utf8",
    "plan":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/plan?charset=utf8"
}


