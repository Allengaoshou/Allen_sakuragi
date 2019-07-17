#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template,url_for,request,flash,redirect,session,make_response
from utils.pagination import Pagination
from utils.BackendRedis import RedisClient
from utils.HttpParser import Client
from dateutil.relativedelta import relativedelta
from utils.RrdLogger import RrdLogger
from case_manager import app,db
from model.User import User_
from model.Local_db import Link_home,Category,Duty,User,Case_info
from model.Marketing import Marketing_activity
from model.Plan import Finance_plan,Uplan_repay_record
from model.Jimu_db import Node_activity,Jimu_prize,Node_activity_withdraw
import redis

import json
import time
import os
import datetime
import sys

# import importlib

reload(sys)
sys.setdefaultencoding('utf-8')
# app = Flask(__name__)
#
# app.secret_key = 'some_secret'



# app.config['SECRET_KEY'] = 'hard to guess string'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/dutylist?charset=utf8'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:1234@localhost:3306/dutylist?charset=utf8'
# app.config['SQLALCHEMY_BINDS'] ={
#     "jimu":"mysql+pymysql://root:123123@172.16.3.173:3306/node_jimu_system?charset=utf8",
#     "ywcs":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/renrendai_0513?charset=utf8",
#     "marketing":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.82:3306/marketing?charset=utf8",
#     "hxb":"mysql+pymysql://root:yZT0b6m32UDg@172.16.4.122:3306/renrendai_0513?charset=utf8"
# }
# db = SQLAlchemy(app)
UPLOAD_PATH = os.path.split(os.path.realpath(__file__))[0]


@app.route('/logout')
def logout():
    try:
        session.pop('user_id', None)
        session.pop('username', None)
        session.clear()
    except Exception as e:
        return e
    return redirect(url_for('login'))

@app.route('/login',methods=['GET', 'POST'])
def login():
    myname = None
    next = None
    # refer_list = []
    # refer = str(request.referrer).split('/')[-1]

    if request.method == "POST":
        phone = request.form['phone']
        password = request.form['password']
        if phone or password:
            user = User.query.filter_by(phone=phone).first()
            if user is not None:
                if user.password != password:
                    flash('Password or Phone is not ture')
                    return redirect(url_for('login'))
                else:
                    session['user_id'] = user.user_id
                    session['username'] = user.username

                    return redirect(url_for('home'))
            else:
                flash('Password or Phone is not ture')
                return redirect(url_for('login'))

        else:
            flash('field can not be empty')
            return redirect(url_for('login'))
    else:
        return render_template('login.html',myname = myname)


@app.route('/register',methods=['GET', 'POST'])
def register():
    myname = None
    if request.method == "POST":
        username = request.form['username']
        phone = request.form['phone']
        password = request.form['password']
        repassword = request.form['repassword']

        if username or phone or password or repassword:
            if password != repassword:
                flash('Password and Confirm Password not same')
                return redirect(url_for('register'))
            res = User.query.filter_by(phone=phone).first()
            if res:
                flash('phone is be register')
                return redirect(url_for('register'))
            data = User(username,phone,password,(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
            res = db.session.add(data)
            db.session.commit()
            if data.user_id:
                flash('register successfully! please login')
                return redirect(url_for('login'))
            else:
                flash('register error!')
                return redirect(url_for('register'))
        else:
            flash('field can not be empty')
            return redirect(url_for('register'))
    else:
        return render_template('register.html',myname = myname)


@app.route('/addlink',methods=['GET', 'POST'])
def addlink():
    myname = None
    # link_to_service = 'UI'
    # if request.method == "GET":
    # if 'user_id' not in session:
        # return redirect(url_for('login'))
    # 	else:
    # 		# sql = 'select * from du_link where du_link.link_belong_service = %s  ORDER BY du_link.link_id DESC ' % link_to_service
    # 		# links = db.session.execute(sql).fetchall()
    # 		myname = session['username']
    # 		return render_template('index.html',myname=myname)
    if request.method == "POST":
        link_name = request.form['link_name']
        print (link_name)
        link_belong_service = request.form['link_belong_service']
        link_address = request.form['link_address']

        if link_name and link_belong_service and link_address:
            data = Link_home(link_name=link_name,link_address=link_address,link_belong_service=link_belong_service,update_time =(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
            res = db.session.add(data)
            db.session.commit()
            flash('add successfully! ')

            return redirect(url_for('home'))

        else:
            flash('field can not be empty')
            return redirect(url_for('addlink'))
    else:
        myname = session['username']
        # link_name = request.form['link_name']
        print ("here")
        return render_template('add_link.html',myname=myname)



@app.route('/',methods=['GET', 'POST'])
def home():
    myname = None
    links = {"link_toUI" :"%UI%",
    "link_touser":"%user%",
     "link_toplan": "plan",
    "link_toloan":"%loan%",
    "link_topay":"pay",
    "link_torepay":"repay"}

    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        qa =['allen','liuwei','liuchengwei','pengying']
        sql_ui = 'select * from du_link where du_link.link_belong_service LIKE "{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_toUI"))
        links_toUI = db.session.execute(sql_ui).fetchall()
        sql_touser = 'select * from du_link where du_link.link_belong_service LIKE"{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_touser"))
        links_touser = db.session.execute(sql_touser).fetchall()
        sql_toloan = 'select * from du_link where du_link.link_belong_service   LIKE "{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_toloan"))
        links_toloan = db.session.execute(sql_toloan).fetchall()
        sql_topay = 'select * from du_link where du_link.link_belong_service LIKE "{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_topay"))
        links_topay = db.session.execute(sql_topay).fetchall()
        sql_torepay = 'select * from du_link where du_link.link_belong_service LIKE "{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_torepay"))
        links_torepay = db.session.execute(sql_torepay).fetchall()
        sql_toplan = 'select * from du_link where du_link.link_belong_service LIKE "{}"  ORDER BY du_link.link_id DESC '.format(links.get("link_toplan"))
        links_toplan = db.session.execute(sql_toplan).fetchall()
        myname = session['username']
        disabled = "green" if myname in qa else "disabled"
        return render_template('index.html',disabled=disabled,myname=myname, links_toUI=links_toUI, links_touser=links_touser, links_toloan=links_toloan, links_topay=links_topay, links_torepay=links_torepay, links_toplan=links_toplan)


@app.route('/add_duty',methods=['GET','POST'])
def add_duty():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:

        myname = session['username']
        if request.method == "POST":
            title = request.form['title']
            print (title)
            category_id = request.form['name']
            is_show = request.form['is_show']
            status = request.form['status']
            parm = ''
            return_parm = ''
            if title and category_id:
                data = Duty(category_id,session['user_id'],parm,return_parm,title,status,is_show,(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
                res = db.session.add(data)
                db.session.commit()
                print (data.duty_id)
                if data.duty_id:
                    flash('add successfully! ')
                    return redirect(url_for('my_duty'))
                else:
                    flash('register error!')
                    return redirect(url_for('add_duty'))
            else:
                flash('field can not be empty')
                return redirect(url_for('add_duty'))
        else:
            print(request.referrer)
            category_list = Category.query.order_by(Category.category_id).all()
            return render_template('add_duty.html',category_list = category_list)

@app.route('/my_duty',methods=['GET', 'POST'])
def my_duty():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        total_sql = 'select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = %s' % session['user_id']
        duty_list_all = db.session.execute(total_sql).fetchall()
        if request.method == 'GET' and request.args.get('category_id'):
            category_id = request.args.get('category_id')
            sql = 'select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where t1.user_id = %s  and t1.category_id = %s ' % (session['user_id'],category_id)
            print(len(duty_list_all))
            li = []
            for i in range(1, len(duty_list_all) + 1):
                li.append(i)
            pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=3)
            html = pager_obj.page_html()
            return render_template('my_duty.html',duty_list=duty_list, myname=myname, html=html)

        elif request.method == 'POST':
            category_list = Category.query.order_by(Category.category_id).all()
            print(len(duty_list_all))
            li = []
            for i in range(1, len(duty_list_all) + 1):
                li.append(i)
            pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=3)
            page = int(int(request.args.get("page")) - 1)
            page_corresponding_num = int(page*3)
            # print(request.path)
            # print(request.args)
            index_list = li[pager_obj.start:pager_obj.end]
            a = [str(x) for x in index_list]
            # b = ",".join(a)
            # print(b)
            # print(type(b))
            print(index_list)
            print(type(index_list))
            html = pager_obj.page_html()
            sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = %s ORDER BY t1.duty_id limit %s,3" % (session['user_id'],page_corresponding_num)

            # sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = {} and t1.duty_id in ({index_list})".format(session['user_id'],index_list=index_list)
            duty_list = db.session.execute(sql1).fetchall()
            return render_template('my_duty.html', duty_list=duty_list, category_list=category_list, myname=myname, html=html)

        else:
            category_list = Category.query.order_by(Category.category_id).all()
            # print("here")
            li = []
            for i in range(1, len(duty_list_all) + 1):
                li.append(i)
            pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=3)
            ###登录用户自己名下的case
            if request.args.get("page") is not None and request.args.get("suite") is None:
                page = int(int(request.args.get("page")) - 1)
                page_corresponding_num = int(page*3)
                # print(request.path)
                # print(request.args)
                index_list = li[pager_obj.start:pager_obj.end]
                # a = [str(x) for x in index_list]
                # b = ",".join(a)
                # print(index_list)
                # print(type(index_list))
                html = pager_obj.page_html()
                sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = %s ORDER BY t1.duty_id DESC limit %s,3" % (session['user_id'],page_corresponding_num)
                duty_list = db.session.execute(sql1).fetchall()
                print("ggg")
                return render_template('my_duty.html', duty_list=duty_list, category_list=category_list, myname=myname,
                                       html=html)
            ###查询公共的case
            else:
                ###search button 下逻辑
                if request.args.get('suite') is not None:
                    category_id = request.args.get('suite')
                    sql2 = 'select du_duty.*,du_category.name from du_duty  left join du_category on du_category.category_id = du_duty.category_id where du_duty.category_id = %s and du_duty.is_show = 1 ORDER BY du_duty.duty_id DESC ' % category_id
                    duty_list1 = db.session.execute(sql2).fetchall()
                    ###search 情况含page 参数
                    if request.args.get("page") is not None:
                        print("gg")
                        ki = []
                        for i in range(1, len(duty_list1) + 1):
                            ki.append(i)
                        pager_obj = Pagination(request.args.get("page", 1), len(ki), request.path, request.args,
                                               per_page_count=3)
                        page = int(int(request.args.get("page")) - 1)
                        page_corresponding_num1 = int(page * 3)
                        html = pager_obj.page_html()
                        sql3 = 'select du_duty.*,du_category.name from du_duty  left join du_category on du_category.category_id = du_duty.category_id where du_duty.category_id = %s and du_duty.is_show = 1 ORDER BY du_duty.duty_id DESC limit %s,3' % (category_id,page_corresponding_num1)
                        duty_list3 = db.session.execute(sql3).fetchall()
                        return render_template('my_duty.html', duty_list=duty_list3, category_list=category_list,myname=myname, html=html)
                    ###search 情况不含page 参数
                    else:
                        ki = []
                        for i in range(1, len(duty_list1) + 1):
                            ki.append(i)
                        pager_obj = Pagination(request.args.get("page", 1), len(ki), request.path, request.args,
                                               per_page_count=3)
                        # page = int(int(request.args.get("page")) - 1)
                        # page_corresponding_num1 = int(page * 3)
                        html = pager_obj.page_html()
                        sql3 = 'select du_duty.*,du_category.name from du_duty  left join du_category on du_category.category_id = du_duty.category_id where du_duty.category_id = %s and du_duty.is_show = 1 ORDER BY du_duty.duty_id DESC limit 3' % category_id
                        duty_list = db.session.execute(sql3).fetchall()
                        return render_template('my_duty.html', duty_list=duty_list, category_list=category_list,myname=myname, html=html)
                else:
                    print("1")
                    # print(request.args)
                    html = pager_obj.page_html()
                    sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id =%s ORDER BY t1.duty_id DESC limit 3" % session['user_id']
                    duty_list = db.session.execute(sql1).fetchall()
                    return render_template('my_duty.html', duty_list=duty_list, category_list=category_list,
                                           myname=myname, html=html)
        return render_template('my_duty.html',duty_list = duty_list,category_list=category_list,myname=myname,html=html)

@app.route('/add_category',methods=['GET', 'POST'])
def add_category():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        myname = session['username']
        if request.method == 'POST':
            name = request.form['name']
            if name:
                res = Category.query.filter_by(name=name).first()
                if res:
                    flash('catgory is here')
                    return redirect(url_for('add_category'))
                else:
                    data = Category(name)
                    res = db.session.add(data)
                    db.session.commit()
                    return redirect(url_for('my_duty'))
            else:
                flash('name could not be None!')
                return render_template('add_category.html')

        return render_template('add_category.html' ,username=session['username'],myname=myname)


@app.route('/premium_renewal',methods=['GET', 'POST'])
def premium_renewal():
    print('22')
    DEFAULT_POST_HEADER = {'content-type': "application/x-www-form-urlencoded;charset=UTF-8"}
    DEFAULT_JSON_HEADER = {'content-type': "application/json;charset=UTF-8"}
    client = Client()
    logger = RrdLogger().getLogger('premium_renewal')
    beginResellingTime = time.strftime("%Y-%m-%d %H:%M:%S")
    endSellingTimeStr_compatible = datetime.datetime.now() + datetime.timedelta(days=1)
    endSellingTimeStr = endSellingTimeStr_compatible.strftime("%Y-%m-%d %H:%M:%S")
    quitTime_compatible = datetime.datetime.now() + datetime.timedelta(days=367)
    quitTime = quitTime_compatible.strftime("%Y-%m-%d %H:%M:%S")
    empty = ""
    # end_lockingtime_math = (datetime.datetime.now() + datetime.timedelta(days=367) - datetime.timedelta(days=419) ).strftime("%Y-%m-%d %H:%M:%S")
    # beginResellingTime_math = (datetime.datetime.now() - datetime.timedelta(days=420)).strftime("%Y-%m-%d %H:%M:%S")
    # endSellingTimeStr_math =  (endSellingTimeStr_compatible - datetime.timedelta(days=419)).strftime("%Y-%m-%d %H:%M:%S")
    # due_date_compatible = endSellingTimeStr_compatible - datetime.timedelta(days=419) + relativedelta(days=+1) + relativedelta(months=+1)

    if request.method == 'POST':
        Days = request.form['advanced_days']
        DaysADD = int(Days) + 1
        end_lockingtime_math = (
                    datetime.datetime.now() + datetime.timedelta(days=367) - datetime.timedelta(days=int(Days))).strftime(
            "%Y-%m-%d %H:%M:%S")
        beginResellingTime_math = (datetime.datetime.now() - datetime.timedelta(days=int(DaysADD))).strftime(
            "%Y-%m-%d %H:%M:%S")
        endSellingTimeStr_math = (endSellingTimeStr_compatible - datetime.timedelta(days=int(Days))).strftime(
            "%Y-%m-%d %H:%M:%S")
        due_date_compatible = endSellingTimeStr_compatible - datetime.timedelta(days=int(Days)) + relativedelta(
            days=+1) + relativedelta(months=+1)
        due_date = due_date_compatible.strftime("%Y-%m-%d %H:%M:%S")
        mobile = request.form['phonenum']
        # data = {'env': 'YWCS','category': int(2),'beginResellingTime': beginResellingTime,'amount': int(20000),'isPlanTime':bool(1),'reserveAmount': int(0),'reserveTime':empty,'name': 'gao优选{}期'.format(beginResellingTime),'endSellingTimeStr': endSellingTimeStr,'quitTime': quitTime,'compoundRate': float(10),'baseInterestRate': float(10),'extraInterestRate': float(0),'financePlanType': 'PREMIUM','style':empty, 'countDownType': int(0), 'tag': '到期后转入自由服务期','expectedRateUplan': float(10),'contractId': int(108),'minRegisterAmount': int(1000),'singleMaxRegisterAmount': int(20000),'registerMultipleAmount': int(1000),'salePeriod': int(2),'lockPeriod': int(12),'finalPeriod': int(18),'applyQuitDays': int(5),'quitRateAdvance': int(2),'maxUcodeAmount': int(0),'products': int(26),'allowAdvanceQuit': int(1),'introduce': 'hi','minInvestRate': float(30),'minInvestAmount': float(100),'maxInvestRate': float(60),'loanLowestRate': float(15),'loanHighestRate': float(30),'loanLowestPeriod': int(6),'loanHightestPeriod': int(24)}
        data = {'env': 'YWCS','category': '2','beginResellingTime': beginResellingTime,'amount': 20000,'isPlanTime':bool(1),'reserveAmount': 0,'reserveTime':empty,'name': '**Premium**{}'.format(beginResellingTime),'endSellingTimeStr': endSellingTimeStr,'quitTime': quitTime,'compoundRate': 10,'baseInterestRate': 10,'extraInterestRate': 0,'financePlanType': 'PREMIUM','style':empty, 'countDownType': 0, 'tag': 'Transfer to free service after expiration','expectedRateUplan': 10,'contractId': 108,'minRegisterAmount': 1000,'singleMaxRegisterAmount': 20000,'registerMultipleAmount': 1000,'salePeriod': 2,'lockPeriod': 12,'finalPeriod': 36,'applyQuitDays': 5,'quitRateAdvance': 2,'maxUcodeAmount': 0,'products': 26,'allowAdvanceQuit': int(1),'introduce': 'hi','minInvestRate': 30,'minInvestAmount': 100,'maxInvestRate': 60,'loanLowestRate': 15,'loanHighestRate': 30,'loanLowestPeriod': 6,'loanHightestPeriod': 24}
        request_instance = {'method': "GET", 'request_url': 'http://qa.dtc.we.com/tools/addplan/addUplan','parameter':data}
        response = client.proc_request(request_instance)
        if not response is None:
            planid = response.json()[0].get("id")
            # flash(planid)
            if planid != '':
                # mobile = '15202480524'
                userInfo = str(User_.query.filter(User_.mobile == mobile).first())
                userid = userInfo
                userId = int(userid)
                logger.info("userid:{}".format(userInfo))
                data_buy = {'env': 'YWCS','planId':planid,'amount':'{}'.format(request.form['amount']),'cashType':'INVEST','isUX':bool(1),'bank':'MS','user':mobile}
                for i in range(3):
                    request_instance_buy = {'method': "GET", 'request_url': 'http://qa.dtc.we.com/tools/buy/Uplan','parameter': data_buy}
                    response_buy = client.proc_request(request_instance_buy)
                    if response_buy.status_code == 200 and response_buy.json()["result"] == "购买成功":
                        break
                    elif response_buy.status_code == 200:
                        time.sleep(15)
                        continue
                    else:
                        logger.info("购买失败")
                        return render_template('premium_renewal.html', getpremium="购买失败")
                ##根据planid、userid查询subpointid

                get_subpointid_data = {'financePlanId':planid,'userId':"{}".format(userId)}
                get_subpointid_byinterface = {'method': "GET", 'request_url': 'http://172.16.4.92:8680/financePlan/subPoint/detail.j','parameter': get_subpointid_data}
                for i in range(40) :
                    subpointid_response = client.proc_request(get_subpointid_byinterface)
                    time.sleep(5)
                    if subpointid_response.json()["status"] == 0 :
                        break
                    else:
                        continue
                subpointid = subpointid_response.json()["data"]["financePlanVo"]["financeSubPointId"]    ##.get("financePlanVo").get("financeSubPointId")
                # flash(subpointid)
                if not subpointid is None :
                    Finance_plan.query.filter(Finance_plan.id == planid).update({Finance_plan.begin_selling_time:beginResellingTime_math,Finance_plan.status:'PURCHASE_END',Finance_plan.plan_begin_selling_time:beginResellingTime_math,Finance_plan.end_selling_time:endSellingTimeStr_math,Finance_plan.begin_reselling_time:beginResellingTime_math,Finance_plan.end_locking_time:end_lockingtime_math})
                    db.session.commit()
                    Uplan_repay_record.query.filter(Uplan_repay_record.sub_point_id == subpointid).update({Uplan_repay_record.due_date: due_date})
                    db.session.commit()
                    generate_repay_record_data = {'subPointId':subpointid}
                    get_uplan_repay_record ={'method': "GET", 'request_url': 'http://172.16.4.92:8680/test/uplan_repay_record.j','parameter': generate_repay_record_data}
                    requests_status = client.proc_request(get_uplan_repay_record).json()["status"]
                    if requests_status == 0:
                        flash("job finished")
                        return render_template('premium_renewal.html', getpremium=client.proc_request(get_uplan_repay_record).json()["message"])
                    else:
                        logger.info("repay_record generate failed")
                        flash("job failed")
                        return redirect(url_for('premium_renewal'))
            else:
                flash("计划发布失败")
                return render_template('premium_renewal.html',getpremium=client.proc_request(get_uplan_repay_record).json()["id"])

        else:
            logger.info("interface:{} response failed".format(Request_instance["request_url"]))
            return redirect(url_for('premium_renewal'))
    else:
        return render_template('premium_renewal.html')


@app.route('/marketing_activity_withdraw', methods=['POST','GET'])
def marketing_activity_withdraw():
    # print("gg")
    # coupon_type = 'select J.name from Jimu_prize as J  where J.groupId = 36 and J.type = 3 ORDER BY J.id '
    # origin_list = db.session.execute(coupon_type).fetchall()
    coupon_list_sqlresult = db.session.execute("select J.name from prize as J  where J.groupId = 34 and J.type = 3 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    couponlist = {i[0] for i in coupon_list_sqlresult}
    print(couponlist)
    cash_list_sqlresult = db.session.execute("select J.name from prize as J  where J.groupId = 34 and J.type = 5 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    cashlist = {i[0] for i in cash_list_sqlresult}
    matter_list_sqlresult = db.session.execute("select J.name from prize as J  where J.groupId = 34 and J.type = 2 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    matterlist = {i[0] for i in matter_list_sqlresult}
    score_list_sqlresult = db.session.execute("select J.name from prize as J  where J.groupId = 34 and J.type = 4 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    scorelist = {i[0] for i in score_list_sqlresult}

    # origin_list = db.session.execute(Jimu_prize.query.filter(Jimu_prize.groupId == 34).filter(Jimu_prize.type == 3), bind=db.get_engine(app, bind="jimu")).fetchall()
    # print(coupon_list)
    myname = session['username']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            hobby = request.form.getlist('checkbox2')
            print(hobby)
            return redirect(url_for('home'))
        else:
            return render_template('marketing_activity_withdraw.html' ,myname=myname,couponlist=couponlist,cashlist=cashlist,matterlist=matterlist,scorelist=scorelist)


@app.route('/marketing_investcashback', methods=['POST','GET'])
def marketing_investcashback():
    # print("gg")

    # jinlist = ['jin1','jin2','jin3']
    myname = session['username']
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        if request.method == "POST":
            hobby = request.form.getlist('checkbox2')
            print(hobby)
            return redirect(url_for('home'))
        else:
            return render_template('marketing_investcashback.html' ,myname=myname,jinlist=origin_list)



@app.route('/marketing_activity/change_activity_begintime',methods=['POST','GET'])
def change_activity_begintime():
    redis_client = RedisClient()
    logger = RrdLogger().getLogger('change_activity_begintime')
    beginTime =(datetime.datetime.now() + datetime.timedelta(seconds=300)).strftime("%Y-%m-%d %H:%M:%S")
    if request.method == 'POST':
        inputparam = request.form.getlist
        print(inputparam)
        activityId = request.form['activityid']
        Node_activity.query.filter(Node_activity.activityId == activityId).update({Node_activity.onlineAt:beginTime})
        db.session.commit()
        logger.info("node时间更新完成")

        redis_connect = redis_client.get_value("MARKETING-ACTIVITY_ID_KEY_{}".format(activityId), "STRING")
        print(redis_connect)
        print('1')
        if redis_connect is not None:
            redis_connect_port = redis_connect[1]
            # redisconn_three = redis.Redis(host='172.16.4.83', port=7003,socket_timeout=3)
            # redisconn_three.delete("MARKETING-ACTIVITY_ID_KEY_{}".format(activityId))
            redisconn_four = redis.Redis(host='172.16.4.83', port=redis_connect_port,socket_timeout=3)
            redisconn_four.delete("MARKETING-ACTIVITY_ID_KEY_{}".format(activityId))
            logger.info("del-redis finished")
            Marketing_activity.query.filter(Marketing_activity.activity_id == activityId).update(
                {Marketing_activity.begin_time: beginTime})
            db.session.commit()
            logger.info("后端时间更新完成")
            # Marketing_activity.query.filter(Marketing_activity.activity_id == activityId).update(
            #     {Marketing_activity.begin_time: beginTime})
            # db.session.commit()
            # logger.info("后端时间更新完成")
            flash("Done")
            return redirect(url_for('change_activity_begintime'))
        else:
            Marketing_activity.query.filter(Marketing_activity.activity_id == activityId).update(
                {Marketing_activity.begin_time: beginTime})
            db.session.commit()
            logger.info("后端时间更新完成")
            flash("Done")
            return redirect(url_for('change_activity_begintime'))
    else:
        return render_template('change_activity_begintime.html')

# @app.route('/ui_schedule_immediately',methods=['POST','GET'])
# def ui_schedule_immediately():
#
#
# @app.route('/ui_schedule',methods=['POST','GET'])
# def ui_schedule():

@app.route('/ui_report', methods=['POST','GET'])
def ui_report():
    print("gg")
    # print(os.path.split(os.path.realpath(__file__))[0])
    #logger.debug('filename is %s' % filename)
    reportfile= datetime.datetime.now().strftime("%Y%m%d")

    # reportfile_path = os.path.join(UPLOAD_PATH, '{}\index.html'.format(reportfile))
    # print(reportfile_path)
    image_data = open(os.path.join(UPLOAD_PATH, 'static\index.html'), "rb").read()
    response = make_response(image_data)
    # print(response)
    response.headers['Content-Type'] = 'text/html; charset=utf-8'
    return response

#************ajax交互begin***********************************************************************************
@app.route('/marketing_activity_couponrate', methods=['POST','GET'])
def marketing_activity_couponrate():
    jinfront = request.get_data().decode("utf-8")
    jindic_sql = db.session.execute("select J.name,J.probability from prize as J  where J.groupId = 34 and J.type = 3 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    jindic = dict(jindic_sql)
    # jindic = {'jin1' : '112','jin2' :'123','jin3' : '345'}
    k = jindic.get(jinfront)
    return str(k)

@app.route('/marketing_activity_cashrate', methods=['POST','GET'])
def marketing_activity_cashrate():
    # jinfront =  request.form.get("coupon")
    jinfront = request.get_data().decode("utf-8")
    jindic_sql = db.session.execute("select J.name,J.probability from prize as J  where J.groupId = 34 and J.type = 5 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    jindic = dict(jindic_sql)
    k = jindic.get(jinfront)
    return str(k)

@app.route('/marketing_activity_matterrate', methods=['POST','GET'])
def marketing_activity_matterrate():
    # jinfront =  request.form.get("coupon")
    jinfront = request.get_data().decode("utf-8")
    jindic_sql = db.session.execute("select J.name,J.probability from prize as J  where J.groupId = 34 and J.type = 2 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    jindic = dict(jindic_sql)
    k = jindic.get(jinfront)
    return str(k)

@app.route('/marketing_activity_scorerate', methods=['POST','GET'])
def marketing_activity_scorerate():
    # jinfront =  request.form.get("coupon")
    jinfront = request.get_data().decode("utf-8")
    jindic_sql = db.session.execute("select J.name,J.probability from prize as J  where J.groupId = 34 and J.type = 4 ORDER BY J.id",bind=db.get_engine(app, bind="jimu")).fetchall()
    jindic = dict(jindic_sql)
    k = jindic.get(jinfront)
    return str(k)


@app.route('/js_call', methods=['GET', 'POST'])
def js_call():
    print('gg')
    print (request.values['text'])
    dict = {"ip":"20","info":"success"}
    dict_tojson = json.dumps(dict)
    time.sleep(5)
    # to send the command by ssh : os.system("ssh user@host \' restart(command) \' ")
    return dict_tojson


@app.route('/case_info_ajax', methods=['GET', 'POST'])
def case_info_ajax():
    duty_id = request.form.get('duty_id')
    print(duty_id)
    # duty_id = request.get_data().decode("utf-8")
    # duty_id = request.form.get('duty_id')
    # print(duty_id)
    # print(caseinfo)
    caseinfo = str(Duty.query.filter(Duty.duty_id==duty_id).all()[0])
    print(caseinfo)
    # dict_tojson = json.dumps(caseinfo_str)
    # sql1 = 'select create_user,case_belong_suite,case_param from du_case  where casename = "{}" '.format(case_name)
    # caseinfo = db.session.execute(sql1).fetchall()
    return caseinfo


@app.route('/case_info_update_ajax', methods=['GET', 'POST'])
def case_info_update_ajax():

    case_info_front = request.get_data().decode("utf-8")
    duty_id = request.form.get('duty_id')
    parm  = str(request.form.get('parameter'))
    # print(type(case_name))
    sql1 = Duty.query.filter(Duty.duty_id == duty_id).update({Duty.parm: parm})
    db.session.commit()

    # # caseinfo_dict = dict(caseinfo)
    # dict_tojson = json.dumps(caseinfo)
    # # sql1 = 'select create_user,case_belong_suite,case_param from du_case  where casename = "{}" '.format(case_name)
    # # caseinfo = db.session.execute(sql1).fetchall()

    return parm

#************ajax交互end***********************************************************************************
# @app.route('/marketing_activity', methods=['POST','GET'])
# def marketing_activity():
#     # print("gg")
#
#     jinlist = ['jin1','jin2','jin3']
#     myname = session['username']
#     if 'user_id' not in session:
#         return redirect(url_for('login'))
#     else:
#         if request.method == "POST":
#             hobby = request.form.getlist('checkbox2')
#             print(hobby)
#             return redirect(url_for('home'))
#         else:
#             return render_template('marketing_activity.html' ,myname=myname,jinlist=jinlist)





# @app.route('/hello')
# def hello():
# 	return "hello"

# @app.route('/do_something_and_redirect')
# def do_something():
# 	return redirect_back()
#
# def redirect_back(default='login', **kwargs):
# 	for target in request.args.get('next'), request.referrer:
# 		if not target:
# 			continue
# 		if is_safe_url(target):
# 			return redirect(target)
# 	return redirect(url_for(default, **kwargs))
#
# def is_safe_url(target):
# 	ref_url = urlparse(request.host_url)
# 	test_url = urlparse(urljoin(request.host_url, target))
# 	return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# @app.errorhandler(404)
# def page_not_found(e):
# 	myname = None
# 	if 'user_id' in session:
# 		myname = session['username']
# 	return render_template('404.html',myname=myname), 404
# @app.errorhandler(500)
# def internal_server_error(e):
# 	myname = None
# 	if 'user_id' in session:
# 		myname = session['username']
# 	return render_template('500.html',myname=myname), 500

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0',port=8080)