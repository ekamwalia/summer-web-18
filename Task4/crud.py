import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "cruddb.db"))
app=Flask (__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Movie (db.Model):
    title=db.Column(db.String(80), primary_key=True)

    def __init__(self, title):
        self.title=title

@app.route ("/")
def home ():
    return "Create, Read, Update, Delete movie titles"

@app.route ("/create", methods= ["GET", "POST"])
def create ():
    movie=Movie(request.json["title"])
    db.session.add (movie)
    db.session.commit ()
    return "Added "+str (movie.title)

@app.route("/read", methods=['GET', 'POST'])
def read ():
    allmovies=[]
    movies=Movie.query.order_by('Movie.title').all ()
    for m in movies:
        allmovies.append(m.title)
    return jsonify (allmovies)

@app.route ("/update", methods=["GET","POST"])
def update ():
    updateinfo=request.json
    newtitle=updateinfo["newtitle"]
    oldtitle=updateinfo["oldtitle"]
    movie=Movie.query.filter_by(title=oldtitle).first()
    if movie is None:
        return "Movie does not exist in database"
    movie.title=newtitle
    db.session.commit ()
    return ( "Updated " + oldtitle +" to " + newtitle)

@app.route("/delete", methods=['GET', 'POST'])
def delete ():
    delinfo=request.json["title"]
    movie=Movie.query.filter_by(title=delinfo).first()
    if movie is None:
        return "Movie does not exist in database"
    db.session.delete(movie)
    db.session.commit ()
    return "Deleted " + delinfo

if __name__=="__main__":
    app.run(debug=True)
