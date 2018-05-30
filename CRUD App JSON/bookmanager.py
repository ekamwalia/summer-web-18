import os

from flask import Flask
# from flask import render_template
from flask import request,jsonify
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir,"bookdatabase.db"))

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=database_file

db=SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=False, nullable=False, primary_key=True)

    def __init__(self, title):
    	self.title=title
    

book_data={"title": ""}
default_data=[]

@app.route("/", methods=["GET","POST"])
def home():

	book = request.json['title']
	new_book=Book(book)
	db.session.add(new_book)
	db.session.commit()
	book_data['title']=new_book.title
	return jsonify(book_data["title"])

@app.route("/all", methods=["GET", "POST"])
def all():
	books=Book.query.all()
	for i in books:
		default_data.append(str(i.title))
	return jsonify(default_data)


@app.route("/update", methods=["POST"])
def update():

	newtitle = request.json['newtitle']
	oldtitle = request.json['oldtitle']
	books = Book.query.filter_by(title=oldtitle).first()
	books.title=newtitle
	db.session.commit()
	book_data['title']=books.title
	return jsonify(book_data["title"])


@app.route("/delete", methods=["POST"])
def delete():
	title = request.json.get("title")
	book = Book.query.filter_by(title=title).first()
	db.session.delete(book)
	db.session.commit()

	book_data['title']=book.title
	return jsonify(book_data["title"])


if __name__ == '__main__':
	app.run(debug=True)