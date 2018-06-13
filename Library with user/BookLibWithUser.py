import os
from flask import Flask, jsonify, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import json
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)


project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"library.db"))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file

db=SQLAlchemy(app)

log=False
currentUser=''
"""
UserID=admin
password=admin

UserID=khator
password=asd1234

"""

class books(db.Model):
	book_name=db.Column(db.String(30), primary_key=True, nullable=False)
	rating=db.Column(db.Float(4,1))
	availability=db.Column(db.String(3))

	def __init__(self, book_name ,rating, availability):
		self.book_name=book_name
		self.rating=rating
		self.availability=availability


class Users(db.Model):
	userID=db.Column(db.String(20), primary_key=True,nullable=False)
	uname=db.Column(db.String(20))
	password=db.Column(db.String(20), nullable=False)
	bookIssued=db.Column(db.String(30))

	def __init__(self,userID,uname,password,bookIssued):
		self.userID=userID
		self.uname=uname
		self.password=generate_password_hash(password)
		self.bookIssued=bookIssued

@app.route("/login", methods=["get","Post"])
def login():
	global log, currentUser
	if log:
		return "Already Logged in"
	Id=request.json["userid"]
	Pass=request.json['password']
	user=Users.query.filter_by(userID=Id).first()
	if user is None:
		return "Invalid UserID"
	if check_password_hash(user.password, Pass):
		currentUser=Id
		log=True
		session["user"]=Id
		return "Login Successfull"
	else:
		return "Invalid Password"

@app.route("/")

def home():
	if "user" in session:
		return "Welcome To e-Library\n\tChoose one of the following:\n\t\tall\n\t\tadd\n\t\tissue\n\t\treturn\n\t\tdelete"
	else:
		return "Please Login\nTo login go to /login"

@app.route("/all", methods=["Get"])

def all():
	all_books=[]
	all_rate=[]
	abooks=books.query.all()

	for i in abooks:
		all_books.append({"book_name":i.book_name,"rating":str(i.rating),"availability":i.availability})
	
	return jsonify(all_books)

@app.route("/add", methods=["Get","Post"])

def add():
	if "user" in session:
		if currentUser=="admin":

			book_detail=books(request.json['book_name'], request.json['rating'], request.json['availability'])
			db.session.add(book_detail)
			db.session.commit()

			return "Book added-"+str(book_detail.book_name)
		else:
			return "Sorry! Only admin can add a book"
	return "Not logged in, Please log in first"+redirect(url_for('login'))

@app.route("/issue", methods=["Get","Post"])

def issue():
	if "user" in session:
		user=Users.query.filter_by(userID=currentUser).first()
		if not user.bookIssued:
			n=request.json['name']
			bname=books.query.filter_by(book_name=n).first()
			abooks=books.query.all()

			if bname is None:
				return "enter VALID book name"
			
			for i in abooks:
				if i.book_name==bname.book_name:
					if i.availability=="yes":
						i.availability="no"
						user.bookIssued=bname.book_name
						db.session.commit()
						return "Book Successfull Issued"
					
			return "Book Already Issued"
		else:
			return "You can only issue One book at a time"
	else:
		return "Please Login first"+redirect(url_for("login"))

@app.route('/return', methods=["Get","Post"])

def ReturnBook():
	if "user" in session:
		n=request.json['name']
		user=Users.query.filter_by(userID=currentUser).first()
		if user.bookIssued==n:
			bname=books.query.filter_by(book_name=n).first()
			abooks=books.query.all()

			if bname is None:
				return "enter VALID book name"
			
			for i in abooks:
				if i.book_name==bname.book_name:
					if i.availability=="no":
						i.availability="yes"
						db.session.commit()
						return "Book Returned Successfull"
					
			return "Book was never Issued"
		return "this book was not issued by you in the first place"
	else:
		return "Please Login first\nTo login go to /login"


@app.route('/delete', methods=['Get','Post'])

def delete():
	if currentUser=="admin":
		n=request.json["name"]
		bname=books.query.filter_by(book_name=n).first()
		if bname is None:
			return "dont worry, book never existed"

		db.session.delete(bname)
		db.session.commit()

		return "book data deleted"
	else:
		return "Sorry! Only admin can delete a book"

@app.route('/signup',methods=['Get','Post'])
@app.route('/addUser',methods=['Get','Post'])

def new_user():
	newUser=Users(request.json["UserID"], request.json["uname"], request.json["password"], "")
	db.session.add(newUser)
	db.session.commit()
	return "user Successfull added\n\nTo login go to /login"

@app.route('/logout', methods=["get","Post"])
def logout():
	log=False
	session.pop("user", None)
	return "Session Logged Out successfully\nTo login again go to /login"

if __name__ == '__main__':
	app.secret_key=os.urandom(15)
	app.run(debug=True)