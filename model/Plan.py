#!/usr/bin/env python
# -*- coding: utf-8 -*-
from case_manager import db


class Finance_plan(db.Model):
    __bind_key__ = 'plan'
    __tablename__ = 'finance_plan'
    id = db.Column(db.Integer,primary_key=True)
    actual_amount = db.Column(db.Float)
    category = db.Column(db.String)
    allow_access = db.Column(db.Integer)
    amount = db.Column(db.Float)
    append_multiple_amount = db.Column(db.Integer)
    begin_selling_time = db.Column(db.DateTime)
    buy_in_rate = db.Column(db.Float)
    cashdraw_day = db.Column(db.Integer)
    cashdraw_isfree = db.Column(db.Integer)
    close_time = db.Column(db.DateTime)
    contract_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)
    create_user = db.Column(db.String)
    end_locking_time = db.Column(db.DateTime)
    end_selling_time = db.Column(db.DateTime)
    expected_rate = db.Column(db.String)
    expected_rate_uplan = db.Column(db.Float)
    interest_rate = db.Column(db.Float)
    introduce = db.Column(db.String)
    loan_highest_rate = db.Column(db.Float)
    loan_hightest_period = db.Column(db.Integer)
    loan_lowest_period = db.Column(db.Integer)
    loan_lowest_rate = db.Column(db.Float)
    lock_period = db.Column(db.Integer)
    max_invest_rate = db.Column(db.Float)
    min_append_amount = db.Column(db.Float)
    min_invest_rate = db.Column(db.Float)
    min_register_amount = db.Column(db.Float)
    name = db.Column(db.String)
    picture = db.Column(db.String)
    products_json = db.Column(db.String)
    quit_rate = db.Column(db.Float)
    quit_rate_advance = db.Column(db.Float)
    register_multiple_amount = db.Column(db.Integer)
    sale_period = db.Column(db.Integer)
    single_max_register_amount = db.Column(db.Float)
    status = db.Column(db.String)
    update_time = db.Column(db.DateTime)
    update_user = db.Column(db.String)
    version = db.Column(db.Integer)
    plan_begin_selling_time = db.Column(db.DateTime)
    min_invest_amount = db.Column(db.Float)
    actual_reserve_amount = db.Column(db.Float)
    max_ucode_amount = db.Column(db.Float)
    deposit_rate = db.Column(db.Float)
    max_deposit_amount = db.Column(db.Float)
    end_reserving_time = db.Column(db.DateTime)
    end_payment_time = db.Column(db.DateTime)
    balance_payment_time = db.Column(db.DateTime)
    begin_reselling_time = db.Column(db.DateTime)
    balance_payment_flag = db.Column(db.String)
    actual_reserving_full_time = db.Column(db.DateTime)
    actual_balance_payment_end_time = db.Column(db.DateTime)
    end_reserving_process_flag = db.Column(db.String)
    contract_rsv_id = db.Column(db.Integer)
    is_roll_over = db.Column(db.Integer)
    novice = db.Column(db.Integer)
    extra_interest_rate = db.Column(db.Float)
    base_interest_rate = db.Column(db.Float)
    tag = db.Column(db.String)
    finance_plan_type = db.Column(db.String)
    compound_rate = db.Column(db.Float)
    weight = db.Column(db.Integer)
    style = db.Column(db.String)
    is_show_amount = db.Column(db.Integer)
    is_show_countdown = db.Column(db.Integer)
    label = db.Column(db.Integer)
    final_period = db.Column(db.Integer)
    apply_quit_days = db.Column(db.Integer)
    reserve_time = db.Column(db.DateTime)
    reserve_amount = db.Column(db.Float)
    allow_advance_quit = db.Column(db.Integer)


    def __repr__(self):
        return '%r' % self.id
        # ,'%r'% self.amount,'%s'% self.amount, '%s'% self.actual_amount, self.loan_highest_rate, self.loan_lowest_rate, self.lock_period,
        # self.category, self.status, self.begin_selling_time, self.weight, self.category, self.end_locking_time,
        # self.finance_plan_type, self.expected_rate, self.name, self.expected_rate_uplan, self.apply_quit_days,
        # self.end_locking_time, self.novice, self.create_time
        # "<finance_plan(id='%s', amount='%s', actual_amount='%r', loan_highest_rate=='%r', loan_lowest_rate=='%r', lock_period='%r', category='%r', status='%r', begin_selling_time='%r'),weight='%r',category='%r',end_locking_time='%r', finance_plan_type='%r', expected_rate='%r', name='%r', expected_rate_uplan='%r', apply_quit_days='%r', end_locking_time-'%s', novice='%s', create_time='%s'>"

class Uplan_repay_record(db.Model):
    __bind_key__ = 'plan'
    __tablename__ = 'uplan_repay_record'
    id = db.Column(db.Integer, primary_key=True)
    sub_point_id = db.Column(db.Integer)
    phase_number = db.Column(db.Integer)
    due_date = db.Column(db.DateTime)
    interest = db.Column(db.Float)
    recovery_interest = db.Column(db.Float)
    unpaid_interest = db.Column(db.Float)
    reminded = db.Column(db.Integer)
    version = db.Column(db.Integer)

    def __repr__(self):
        return "<dun_info(interest='%s', recovery_interest='%s', unpaid_interest='%s', sub_point_id='%s')>" % (
            self.interest, self.recovery_interest, self.unpaid_interest, self.sub_point_id)