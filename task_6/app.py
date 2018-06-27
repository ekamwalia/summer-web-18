from flask import Flask, request, jsonify, session, abort, redirect, flash, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
import os
from flask_login import LoginManager
import requests
import json
import random
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from functools import wraps

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "web_summer_task6_users.db"))
engine = create_engine('sqlite:///web_summer_task6_users.db', echo=True)

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db= SQLAlchemy(app)


class Users(db.Model):

	Username=db.Column(db.String(20), primary_key=True)
	Password=db.Column(db.String(20), nullable=False)
	def __init__(self, Username, Password):
		self.Username=Username
		self.Password=generate_password_hash(Password)
		db.create_all()


class Star(db.Model):
	ID=db.Column(db.Integer(), primary_key=True)
	Username=db.Column(db.String(20))
	starred=db.Column(db.String(20))

	def __init__(self,ID,Username,starred):
		self.ID=ID
		self.Username=Username
		self.starred=starred
		db.create_all()


@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        session.pop("user", None)
        cu=Users.query.filter_by(Username=request.form["Username"]).first()
        if cu is None:
            flash('NO SUCH USER EXISTS','danger')
            return render_template("login.html")
        if check_password_hash(cu.Password, request.form["Password"]):
            session["user"]=request.form["Username"]
            session['logged_in'] = True
            flash('SUCCESSFULLY LOGGED IN','SUCCESS')
            return redirect(url_for('dashboard'))
        else:
            flash('CHECK USERNAME OR PASSWORD','DANGER')
    return render_template("login.html")
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        if request.form["Password"]==request.form["Confpass"]:
            nu=Users(request.form["Username"], request.form["Password"])
            db.session.add(nu)
            db.session.commit()
            flash('You are now registered and can log in', 'success')
        else:
            flash('Username already exists', 'danger')
    return render_template("register.html")

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/dashboard', methods=['POST','GET'])
@is_logged_in
def dashboard():
	if request.method=="POST":
		session.pop('gitName',None)
		gitname=request.form["Gitname"]
		strd=Star.query.filter_by(Username=session["user"]).all()
		try:
			url='https://api.github.com/users/'+gitname+''
		except:
			flash('INVALID GIT NAME','danger')
		button=False
		for s in strd:
			if s.starred==gitname:
				button=True
		usern=requests.get(url).json()
		session['usern']=usern
		session['gitName']=gitname
		session['but']=button
		return render_template("UserInfo.html",detail=usern,status=button)
	return render_template("search.html")

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

@app.route("/star", methods=['GET','POST'])
@is_logged_in
def star():
	gitname=session["gitName"]
	try:
		sadd=Star(random.randint(1,100000),session["user"], gitname)
		db.session.add(sadd)
		db.session.commit()
        #if random no. coinsides
	except:
		sadd=Star(random.randint(1,100000),session["user"], gitname)
		db.session.add(sadd)
		db.session.commit()
	flash('USER STARRED','success')
	return render_template("starred.html")


@app.route("/unstar", methods=['GET','POST'])
@is_logged_in
def unstar():
	gitname=session["gitName"]
	try:
		adel=Star.query.filter_by(Username=session["user"], starred=gitname).first()
		db.session.delete(adel)
		db.session.commit()
        #if random no. coinsides
	except:
		flash('User is not starred','danger')

	flash('User has been unstarred','success')
	return render_template("starred.html")

@app.route("/fav", methods=['GET','POST'])
@app.route("/starred", methods=['GET','POST'])
@is_logged_in
def starred():
	star=Star.query.filter_by(Username=session["user"]).all()
	std=[]
	for s in star:
		std.append(s.starred)
	if not std:
		flash('NO STARRED USERNAMES','danger')
	return render_template("starred.html", stars=std)






if __name__=="__main__":
	app.secret_key = os.urandom(12)
	app.run(debug=True)
	app.config['TEMPLATES_AUTO_RELOAD'] = True
