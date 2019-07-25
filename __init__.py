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

class   YWCS_ENV_Config():
    ENV_NAME = "YWCS Test Environment"
    ENV_KEY_BANK = "VER"
    IS_ONLINE_ENVIRONMENT = False

    ##################################################################################
    # Default Service Interface Configuration for old core structure
    # DO NOT MODIFY ANYTHING BELOW
    GLOBAL_API_REQUEST_TIMEOUT = 60
    MOBILE_SIGN_KEY = "5343b95de4b0ed764fd9001d"
    API_SERVICE_SIGN_KEY = "4324fdfdfewrewfdsfSetew@#$#@sdfd"         # api老系统26友信信贷标  52培训贷标的
    API_SERVICE_SIGN_KEY_YOUXIN = "gphloveglq1413andtangtang5215277"   # api-service服务26友信信贷标  54友信个贷标
    API_SERVICE_SIGN_KEY_PDL = "pdl4fdfdfe1111fdsfSetew#$%!#@gphl"     #55 PDL标的
    MD5_MAPPING = {"xxhb-rrjf": "4324fdfdfewrewfdsfSetew@#$#@sdfd"}

    # OLD TOMCAT INSTANCES
    WE_HOME_URL = "http://www.test.we.com"
    RRD_HOME_URL = "http://www.test.renrendai.com/"
    CONTROLLER_MGMT = "http://172.16.4.84:9090"
    MGMT_URL = CONTROLLER_MGMT + "/mgmt/login.action"

    MOBILE_API = "http://api.test.renrendai.com/4.0"
    MOBILE_LOGIN_API = 'http://api.test.we.com/4.0/login/login.action'


    # P2P Service
    P2P_API_URL = "http://172.16.4.92"
    P2P_API_PORT = "8680"
    RENRENDAI_WEB_P2P_API_URL = "http://172.16.4.92:8680"


    MARKETING_URL = "172.16.4.91"
    COUPON_API_URL = "172.16.4.91"

    COUPON_API_PORT = "8580"

    RENRENDAI_WEB_CONTROLLER = "http://172.16.4.97:28131"
    ##################################################################################
    # Default Service Interface Configuration for New Services Controllers
    # DO NOT MODIFY ANYTHING BELOW

    # Frontend

    # Node
    NODE_API = 'https://api.test.we.com/n2'

    # P2P Service Controller
    SERVICE_CONTROLLER_P2P_API = "http://172.16.4.88:9980"
    SERVICE_CONTROLLER_P2P_PLAN = "http://172.16.4.92:8680"
    SERVICE_CONTROLLER_P2P_LOAN = "http://api.test.we.com/4.0"
    SERVICE_CONTROLLER_P2P_TRANSFER = "http://api.test.we.com/4.0"

    SERVICE_CONTROLLER_REPAY = "172.16.4.89:9980"


    SERVICE_CONTROLLER_USER = "http://172.16.4.87:7777"
    SERVICE_CONTROLLER_ACCOUNT = "http://172.16.4.87:40080"
    DB_SERVICE_ACCOUNT = None
    SERVICE_CONTROLLER_PAY_CENTER = ""
    DB_SERVICE_PAY_CENTER = None
    SERVICE_RULE_ENGINE_API = "http://172.16.4.98:8680"
    DB_RULE_ENGINE = None

    # Score Service
    SERVICE_CONTROLLER_SCORE = "http://172.16.4.98:8780"
    # Coupon and Marketing service
    SERVICE_CONTROLLER_COUPON = "http://172.16.4.91:8581"
    DB_SERVICE_COUPON = None
    SERVICE_CONTROLLER_MARKETING = "http://172.16.4.91:8580"
    DB_MARKETING = None
    # BI-interface-batchSendCoupon 自动发券接口
    BI_BATCHSENDCOUPON_SERVICE = "http://172.16.4.91:8581"
    # daily_activity service 日常活动接口地址
    # 此地址为UAT环境上部署的marketing地址，需要变更成业务测试
    DAILYACTIVITY_SERVICE = "http://172.16.4.91:8580"

    # RenRenCollege service
    RENREN_COLLEGE_SERVICE_API = "http://www.test.we.com/nco/aio"

    # repay Service
    repay_data_WE = "http://172.16.4.88:9980"
    SERVICE_PAY_P2P_API = "http://172.16.4.88:8577"

    # Fund and FOF Service
    FUND_API_URL = "http://172.16.4.83"
    FUND_API_PORT = "5555"
    SERVICE_CONTROLLER_FUND = "http://172.16.4.83:5555"

    # Insurance Service
    INS_API_URL = "http://172.16.4.96"
    INS_API_PORT = "8381"


    # Exchange Service
    EXC_API_URL = "http://172.16.4.90"
    EXC_API_PORT = "8280"


    # Current Service-Combine transaction records
    CUR_API_RECORD_URL = "172.16.4.89"
    CUR_API_RECORD_PORT = "8481"
    SERVICE_CONTROLLER_CURRENT_COMBINE = ""
    DB_CUR_RECORD = None

    redisHost = "172.16.4.83"
