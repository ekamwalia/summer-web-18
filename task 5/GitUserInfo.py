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

@app.route("/login", methods=["Get","Post"])
def login():
	if request.method=="POST":
		session.pop("user", None)
		cu=Users.query.filter_by(userid=request.form["username"]).first()
		if cu is None:
			return "Invalid Username"
		if check_password_hash(cu.password, request.form["password"]):
			session["user"]=request.form["username"]
			return redirect(url_for("search"))
		else:
			return "Check Username or Password"
	return render_template("login.html")

@app.route("/addAccount", methods=["Post","Get"])
def addAccount():
	if request.method=="POST":
		if request.form["password"]==request.form["Confpass"]:
			try:
				nu=Users(request.form["Username"], request.form["password"])
				db.session.add(nu)
				db.session.commit()
				return "User added successfully"
			except:
				return "Username already registered, try again"

	return render_template("AddUser.html")

@app.route("/search", methods=["get","POST"])
def search():
	if "user" in session:
		if request.method=="POST":
			try:
				session.pop('gitName',None)

				gitname=request.form["uid"]
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

				return render_template("UserInfo.html", detail=usern, star=button)
			except:
				return "Invalid Username"
		

		return render_template("SearchBar.html", name=session["user"])
	return (redirect(url_for("login")))


@app.route("/repositories")
def repos():
	if "user" in session:
		gitname=session["gitName"]
		url='https://api.github.com/users/'+gitname+'/repos'
		repos=requests.get(url).json()
		return render_template("repos.html", repos=repos)
	return redirect(url_for("login"))

@app.route("/logout")
def logout():
	session.pop('user',None)
	session.pop("gitName",None)
	return redirect(url_for("login"))

@app.route("/star")
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
	return "User Starred"

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
	return "User Unstarred"

@app.route("/starred")
def starred():
	if "user" in session:
		star=Star.query.filter_by(userid=session["user"]).all()
		std=[]
		for s in star:
			std.append(s.stared)
		if not std:
			return "No Starred Usernames"
		return render_template("starred.html", stars=std)
	return redirect(url_for("login"))

if __name__=="__main__":
	app.secret_key=os.urandom(15)
	app.run(debug=True)
		
