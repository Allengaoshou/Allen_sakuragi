#!/usr/bin/env python
# -*- coding: utf-8 -*-
from case_manager import db

class User_(db.Model):
    __bind_key__ = 'ywcs'
    __tablename__ = 'user_'
    userId = db.Column(db.Integer, primary_key=True)
    basicInfoFinished = db.Column(db.Integer)
    detailInfoFinished = db.Column(db.Integer)
    registerTime = db.Column(db.DateTime)
    roles = db.Column(db.Integer)
    username = db.Column(db.String)
    mobile = db.Column(db.String)
    account_id = db.Column(db.Integer)

    def __repr__(self):
        # return "<user_(userId='%s', mobile='%s', username='%s',registerTime='%s')>" % (
        #     self.userId, self.mobile, self.username, self.registerTime)
        return  "%s"  % self.userId