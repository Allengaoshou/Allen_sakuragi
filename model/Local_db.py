#!/usr/bin/env python
# -*- coding: utf-8 -*-
from case_manager import db

class Case_info(db.Model):
    __tablename__ = "du_case"
    caseid = db.Column(db.Integer, primary_key=True)
    casename = db.Column(db.String(512), unique=True)
    case_param = db.Column(db.String(5000), unique=True)
    case_belong_suite = db.Column(db.String(64), unique=True)
    create_user = db.Column(db.String(64), unique=True)
    create_time = db.Column(db.DateTime, unique=True)
    update_time = db.Column(db.DateTime, unique=True)

    def __init__(self, casename,case_param,case_belong_suite,create_user,create_time):
        self.casename = casename
        self.case_param =case_param
        self.case_belong_suite =case_belong_suite
        self.create_user = create_user
        self.create_time = create_time
    def __repr__(self):
        return self.case_param

class Link_home(db.Model):
    __tablename__ = "du_link"
    link_id = db.Column(db.Integer, primary_key=True)
    link_name = db.Column(db.String(64), unique=True)
    link_address = db.Column(db.String(64), unique=True)
    link_belong_service = db.Column(db.String(64), unique=True)
    update_time = db.Column(db.DateTime, unique=True)

    def __init__(self, link_name,link_belong_service,update_time,link_address):
        self.link_name = link_name
        self.link_belong_service =link_belong_service
        self.link_address =link_address
        self.update_time = update_time
    def __repr__(self):
        return self.link_name

class Category(db.Model):
    __tablename__ = "du_category"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Duty(db.Model):
    __tablename__ = "du_duty"
    duty_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, unique=True)
    user_id = db.Column(db.Integer, unique=True)
    parm = db.Column(db.String(5000), unique=True)
    return_parm = db.Column(db.String(5000), unique=True)
    title = db.Column(db.String(64), unique=True)
    status = db.Column(db.Integer, unique=True)
    is_show = db.Column(db.Integer, unique=True)
    update_time = db.Column(db.DateTime, unique=True)

    # def __init__(self,duty_id, category_id, user_id, parm, return_parm, title, status, is_show, update_time):
    #     self.duty_id = duty_id
    #     self.category_id = category_id
    #     self.user_id = user_id
    #     self.parm = parm
    #     self.return_parm = return_parm
    #     self.title = title
    #     self.status = status
    #     self.is_show = is_show
    #     self.update_time = update_time

    def __init__(self, category_id, user_id, parm, return_parm, title, status, is_show, update_time):
        self.category_id = category_id
        self.user_id = user_id
        self.parm = parm
        self.return_parm = return_parm
        self.title = title
        self.status = status
        self.is_show = is_show
        self.update_time = update_time

    def __repr__(self):
        return self.parm

class User(db.Model):
    __tablename__ = "du_user"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    phone = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64), unique=True)
    update_time = db.Column(db.DateTime, unique=True)

    def __init__(self, username,phone,password,update_time):
        self.username = username
        self.phone = phone
        self.password = password
        self.update_time = update_time

    def __repr__(self):
        return self.username
