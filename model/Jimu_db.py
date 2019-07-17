#!/usr/bin/env python
# -*- coding: utf-8 -*-
from case_manager import db

class Jimu_prize(db.Model):
    __bind_key__ = 'jimu'
    __tablename__ = 'prize'
    id = db.Column(db.Integer,primary_key=True)
    groupId = db.Column(db.Integer)
    name = db.Column(db.String)
    type = db.Column(db.Integer)
    totalNum = db.Column(db.Integer)
    residueNum = db.Column(db.Integer)
    probability = db.Column(db.Integer)
    img = db.Column(db.String)
    imgPc = db.Column(db.String)
    success = db.Column(db.String)
    whiteListRuleId = db.Column(db.String)
    extra = db.Column(db.Integer)
    isDefault = db.Column(db.Integer)
    updatedAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)

    def __repr__(self):
        return '%s' % self.name

class Node_activity(db.Model):
    __bind_key__ = 'jimu'
    __tablename__ = 'activity_def'
    activityId = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String)
    activityType = db.Column(db.Integer)
    investList = db.Column(db.String)
    lockPeriod = db.Column(db.String)
    onlineAt = db.Column(db.DateTime)
    offlineAt = db.Column(db.DateTime)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __repr__(self):
        return '%r' % self.activityId

class Node_activity_withdraw(db.Model):
    __bind_key__ = 'jimu'
    __tablename__ = 'user_daily_draw_times'
    id = db.Column(db.Integer,primary_key=True)
    activityId = db.Column(db.Integer)
    userId = db.Column(db.Integer)
    drawDate = db.Column(db.Integer)
    maxTimes = db.Column(db.Integer)
    drawTimes = db.Column(db.Integer)
    addCalledTimes = db.Column(db.Integer)
    createdAt = db.Column(db.DateTime)
    updatedAt = db.Column(db.DateTime)

    def __repr__(self):
        return '%r' % self.maxTimes,self.drawDate