from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "booksdb.db"))

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db= SQLAlchemy(app)

class Books (db.Model):
    title=db.Column(db.String(80), primary_key=True)


    def __init__(self, title):
        self.title=title
        db.create_all();




@app.route ("/")
def home ():
    return "Add, Display, Edit, Delete books"

@app.route ("/add", methods= ["GET", "POST"])
def add ():
    book = Books(request.json["title"])
    db.session.add (book)
    db.session.commit ()
    return "Added "+str (book.title)

@app.route("/display", methods=['GET', 'POST'])
def read ():
    allbooks=[]
    books=Books.query.order_by('Books.title').all ()
    for i in books:
        allbooks.append(i.title)
    return jsonify (allbooks)

@app.route ("/edit", methods=["GET","POST"])
def update ():
    updateinfo=request.json
    newtitle=updateinfo["newtitle"]
    oldtitle=updateinfo["oldtitle"]
    book=Books.query.filter_by(title=oldtitle).first()
    if book is None:
        return "Book not found in library"
    book.title=newtitle
    db.session.commit ()
    return ( "Updated " + oldtitle +" to " + newtitle)

@app.route("/delete", methods=['GET', 'POST'])
def delete ():
    delinfo=request.json["title"]
    book=Books.query.filter_by(title=delinfo).first()
    if book is None:
        return "Book does not exist in library"
    db.session.delete(book)
    db.session.commit ()
    return "Deleted " + delinfo

if __name__=="__main__":
    app.run(debug=True)
