from flask import Flask, jsonify, session, redirect, url_for, render_template, request
import requests
import os
import json
import random
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"GitHubUser.db"))

app.config["SQLALCHEMY_DATABASE_URI"]=database_file

db=SQLAlchemy(app)

class Users(db.Model):
	userid=db.Column(db.String(20), primary_key=True)
	password=db.Column(db.String(20), nullable=False)
	def __init__(self, userid,password):
		self.userid=userid
		self.password=generate_password_hash(password)


class Star(db.Model):
	ID=db.Column(db.Integer(), primary_key=True)
	userid=db.Column(db.String(20))
	stared=db.Column(db.String(20))

	def __init__(self,ID,userid,stared):
		self.ID=ID
		self.userid=userid
		self.stared=stared
@app.route("/",methods=["Get","Post"])
@app.route("/login", methods=["Get","Post"])
def login():
	title="login"
	if request.method=="POST":
		session.pop("user", None)
		cu=Users.query.filter_by(userid=request.form["username"]).first()
		if cu is None:
			return render_template("login.html", title=title, inuser=True)
		if check_password_hash(cu.password, request.form["password"]):
			session["user"]=request.form["username"]
			return redirect(url_for("search"))
		else:
			return render_template("login.html", title=title, inpass=True)
	return render_template("login.html", title=title)
	"""
	username=raghav
	password=1234
	"""
@app.route("/addAccount", methods=["Post","Get"])
def addAccount():
	title="Add Account"
	if request.method=="POST":
		if request.form["password"]==request.form["Confpass"]:
			try:
				nu=Users(request.form["Username"], request.form["password"])
				db.session.add(nu)
				db.session.commit()
				return "User added successfully"
			except:
				return render_template("AddUser.html", title=title, exist=True)
		else:
			return render_template("AddUser.html", title=title, unmatch=True)

	return render_template("AddUser.html", title=title)

@app.route("/search", methods=["get","POST"])
def search():
	title="search"
	if "user" in session:
		session.pop("usern", None)
		if request.method=="POST":
			try:
				session.pop('gitName',None)

				gitname=request.form["search"]
				strd=Star.query.filter_by(userid=session["user"]).all()
				try:
					url='https://api.github.com/users/'+gitname+''
				except:
					return "Invalid Git Name"
				button=False
				for s in strd:
					if s.stared==gitname:
						button=True

				usern=requests.get(url).json()
				session['gitName']=gitname
				session["usern"]=usern

				return render_template("UserInfo.html",title=title, detail=usern, star=button, found=True)
			except:
				return "ERROR OCCURED WHILE TAKING YOUR REQUEST.\nPLEASE CHECK YOUR INTERNET CONNECTION"
		

		return render_template("SearchBar.html", name=session["user"])
	return (redirect(url_for("login")))


@app.route("/repositories")
def repos():
	title="Repositories"
	if "user" in session:
		gitname=session["gitName"]
		url='https://api.github.com/users/'+gitname+'/repos'
		repos=requests.get(url).json()
		return render_template("repos.html", repos=repos, title=title, page=True)
	return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.pop('user',None)
	session.pop("gitName",None)
	return redirect(url_for("login"))

@app.route("/star", methods=['GET','POST'])
def star():
	if "user" in session:
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
	return render_template("UserInfo.html", detail=session['usern'], star=True, found=True, page=True)

@app.route("/unstar")
def unstar():
	if "user" in session:
		gitname=session["gitName"]
		try:
			adel=Star.query.filter_by(userid=session["user"], stared=gitname).first()
			db.session.delete(adel)
			db.session.commit()
			#if random no. coinsides
		except:
			return "Already Unstarred"
		return render_template("UserInfo.html", detail=session['usern'], star=False, found=True, page=True)
	return redirect(url_for("login"))

@app.route("/starred")
def starred():
	if "user" in session:
		su=True
		star=Star.query.filter_by(userid=session["user"]).all()
		std=[]
		for s in star:
			std.append(s.stared)
		if not std:
			su=False
		return render_template("starred.html", stars=std, title="Starred Users", SUF=su, page=True)
	return redirect(url_for("login"))

if __name__=="__main__":
	app.secret_key=os.urandom(15)
	app.run(debug=True)
		
