import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import json

app=Flask(__name__)


project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"library.db"))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file

db=SQLAlchemy(app)

b_data=[]
avail=""

class books(db.Model):
	#bookID=db.Column(db.Integer(5), primary_key=True, nullable=False)
	book_name=db.Column(db.String(30), primary_key=True, nullable=False)
	rating=db.Column(db.Float(4,1))
	availability=db.Column(db.String(3))

	def __init__(self, book_name ,rating, availability):
		self.book_name=book_name
		self.rating=rating
		self.availability=availability



@app.route("/")

def home():
	return "Welcome To e-Library\n\tChoose one of the following:\n\t\tall\n\t\tadd\n\t\tissue\n\t\treturn\n\t\tdelete"


@app.route("/all", methods=["Get"])

def all():
	all_books=[]
	all_rate=[]
	abooks=books.query.all()

	for i in abooks:
		all_books.append([i.book_name, str(i.rating), i.availability])
	
	return jsonify(all_books)

@app.route("/add", methods=["Get","Post"])

def add():
	book_detail=books(request.json['book_name'], request.json['rating'], request.json['availability'])
	db.session.add(book_detail)
	db.session.commit()

	return "Book added-"+str(book_detail.book_name)

@app.route("/issue", methods=["Get","Post"])

def issue():
	n=request.json['name']
	bname=books.query.filter_by(book_name=n).first()
	abooks=books.query.all()

	if bname is None:
		return "enter VALID book name"
	
	for i in abooks:
		if i.book_name==bname.book_name:
			if i.availability=="yes":
				i.availability="no"
				db.session.commit()
				return "Book Successfull Issued"
			
	return "Book Already Issued"

@app.route('/return', methods=["Get","Post"])

def ReturnBook():
	n=request.json['name']
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

@app.route('/delete', methods=['Get','Post'])

def delete():
	n=request.json["name"]
	bname=books.query.filter_by(book_name=n).first()
	if bname is None:
		return "dont worry, book never existed"

	db.session.delete(bname)
	db.session.commit()

	return "book data deleted"



if __name__ == '__main__':
	app.run(debug=True)