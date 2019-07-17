#-*- coding: utf-8 -*-
#encoding=utf-8
from flask import Flask,render_template,url_for,request,flash,redirect,session
from flask_sqlalchemy import SQLAlchemy
from utils.pagination import Pagination
import time
import datetime
# import importlib
# importlib.reload(sys)
import sys
reload(sys)
sys.setdefaultencoding('utf8')
app = Flask(__name__)

app.secret_key = 'my is some_secret'

# app.config['SESSION_TYPE'] = 'filesystem'

# from sae.const import (MYSQL_HOST, MYSQL_HOST_S,
#     MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB
# )

# app.config['SECRET_KEY'] = 'hard to guess string'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://%s:%s@%s:%s/%s' % (MYSQL_USER, MYSQL_PASS, MYSQL_HOST, MYSQL_PORT, MYSQL_DB)

# app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost:3306/dutylist?charset=utf8'
db = SQLAlchemy(app)

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
	title = db.Column(db.String(64), unique=True)
	status = db.Column(db.Integer, unique=True)
	is_show = db.Column(db.Integer, unique=True)
	create_time = db.Column(db.DateTime, unique=True)
	
	def __init__(self, category_id, user_id, title, status, is_show, create_time):
		self.category_id = category_id
		self.user_id = user_id
		self.title = title
		self.status = status
		self.is_show = is_show
		self.create_time = create_time

	def __repr__(self):
		return self.title
class User(db.Model):
	__tablename__ = "du_user"
	user_id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True)
	phone = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(64), unique=True)
	create_time = db.Column(db.DateTime, unique=True)
	
	def __init__(self, username,phone,password,create_time):
		self.username = username
		self.phone = phone
		self.password = password
		self.create_time = create_time

	def __repr__(self):
		return self.username

@app.route('/',methods=['GET', 'POST'])
def index():
	myname = None
	if 'user_id' in session:
		myname = session['username']
	if request.method == 'GET' and request.args.get('category_id'):
		category_id = request.args.get('category_id')
		sql = 'select t1.*,t2.name,t3.username  from du_duty as t1 left join du_category as t2 on t2.category_id = t1.category_id left join du_user as t3 on t3.user_id = t1.user_id where t1.is_show = 1 and t1.category_id = %s' % category_id		
	else:
		sql = 'select t1.*,t2.name,t3.username  from du_duty as t1 left join du_category as t2 on t2.category_id = t1.category_id left join du_user as t3 on t3.user_id = t1.user_id where t1.is_show = 1'
	duty_list = db.session.execute(sql).fetchall()
	category_list = Category.query.order_by(Category.category_id).all()
	return render_template('index.html',duty_list = duty_list,category_list=category_list,myname = myname)
@app.route('/logout')
def logout():
	session.pop('user_id', None)
	session.pop('username', None)
	return redirect(url_for('index'))
@app.route('/login',methods=['GET', 'POST'])
def login():
	myname = None
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
					return redirect(url_for('my_duty'))
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
			if title and category_id:
				data = Duty(category_id,session['user_id'],title,status,is_show,(datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
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
            print(request.path)
            print(request.args)
            index_list = li[pager_obj.start:pager_obj.end]
            print(index_list)
            html = pager_obj.page_html()
            return render_template('my_duty.html', duty_list=duty_list, category_list=category_list, myname=myname, html=html)

        elif request.method == 'POST':
            print(len(duty_list_all))
            li = []
            for i in range(1, len(duty_list_all) + 1):
                li.append(i)
            pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=3)
            print(request.path)
            print(request.args)
            index_list = li[pager_obj.start:pager_obj.end]
            print(index_list)
            html = pager_obj.page_html()
            return render_template('my_duty.html', duty_list=duty_list, category_list=category_list, myname=myname, html=html)

        else:
        # duty_list = db.session.execute(sql).fetchall()
            category_list = Category.query.order_by(Category.category_id).all()
            print(len(duty_list_all))
            li = []
            for i in range(1, len(duty_list_all) + 1):
                li.append(i)
            pager_obj = Pagination(request.args.get("page", 1), len(li), request.path, request.args, per_page_count=3)
            page = int(int(request.args.get("page")) - 1)
            page_corresponding_num = int(3*int(page))
            # print(request.path)
            # print(request.args)
            index_list = li[pager_obj.start:pager_obj.end]
            a = [str(x) for x in index_list]
            b = ",".join(a)
            print(b)
            print(type(b))
            print(index_list)
            print(type(index_list))
            html = pager_obj.page_html()
            sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = %s order by t1.duty_id desc limit %s,3 " % (session['user_id'],page_corresponding_num)


# sql1 = "select t1.*,t2.name from du_duty as t1  left join du_category as t2 on t2.category_id = t1.category_id where user_id = {} and t1.duty_id in ({index_list})".format(session['user_id'],index_list=index_list)
            duty_list = db.session.execute(sql1).fetchall()
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
					flash('catgory is be here')
					return redirect(url_for('add_category'))
				else:
					data = Category(name)
					res = db.session.add(data)
					db.session.commit()
					return redirect(url_for('my_duty'))
			else:
				flash('name not be None!')
				return render_template('add_category.html')
				
		return render_template('add_category.html' ,username=session['username'],myname=myname)
'''
@app.route('/search',methods=['GET', 'POST'])
def search():
	if request.method == 'GET':
		category_id = request.args.get('category_id')
		sql = 'select du_duty.*,du_category.name,du_user.username  from du_duty  left join du_category on du_category.category_id = du_duty.category_id left join du_user on du_user.user_id = du_duty.user_id where du_duty.is_show = 1 where du_duty.category_id= %s' % category_id
		if session['user_id']:
			sql = 'select du_duty.*,du_category.name from du_duty  left join du_category on du_category.category_id = du_duty.category_id where user_id = %s and du_duty.category_id = %s ' % (session['user_id'],category_id)
			
		duty_list = db.session.execute(sql).fetchall()
		print duty_list
		category_list = Category.query.order_by(Category.category_id).all()
		return render_template('search.html',duty_list = duty_list,category_list=category_list)
	else:
		return redirect(url_for('index'))
'''
@app.errorhandler(404) 
def page_not_found(e):
	myname = None
	if 'user_id' in session:
		myname = session['username']
	return render_template('404.html',myname=myname), 404 
@app.errorhandler(500) 
def internal_server_error(e): 
	myname = None
	if 'user_id' in session:
		myname = session['username']
	return render_template('500.html',myname=myname), 500

if __name__ == '__main__':
	app.run(debug=True)