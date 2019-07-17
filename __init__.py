#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import pymysql
pymysql.install_as_MySQLdb()

#创建项目对象

# import  os
# app.config.from_object('backendqa.config')     #模块下的config文件名，不用加py后缀
app = Flask(__name__, instance_relative_config=False)
default_env = 0
env = "config.py" if default_env == 0 else "hxbconfig.py"
app.config.from_pyfile(env)   # 配置文件

#创建数据库对象
db = SQLAlchemy(app)