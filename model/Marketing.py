#!/usr/bin/env python
# -*- coding: utf-8 -*-
from case_manager import db

class Marketing_activity(db.Model):
    __bind_key__ = 'marketing'
    __tablename__ = 'activity_time_config'
    id = db.Column(db.Integer,primary_key=True)
    activity_id = db.Column(db.String)
    begin_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)


    def __repr__(self):
        return '%r' % self.begin_time