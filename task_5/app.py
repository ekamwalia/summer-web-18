from flask import Flask, request, jsonify, session, abort, redirect,flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, ForeignKey
import os
from flask_login import LoginManager
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "web_summer_users.db"))
engine = create_engine('sqlite:///web_summer_users.db', echo=True)

app= Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db= SQLAlchemy(app)

class Users(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    username=db.Column(db.String(80))
    password=db.Column(db.String(255))
    fullname=db.Column(db.String(50))
    email=db.Column(db.String(50))

    def __init__(self, username, password, fullname, email):
        self.username=username
        self.password=generate_password_hash(password)
        self.fullname=fullname
        self.email=email
        db.create_all()

    '''def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)'''

@app.route('/')
@app.route('/home')
def home():
    if not session.get('logged_in'):
        return "Register user (/register) Login user (/login) Dashboard (/home) Logout (/logout)"
    else:
        return "welcome " + session['username']

@app.route('/register', methods=['GET','POST'])
def create():
    newUser=Users(request.json["username"], request.json["password"], request.json["fullname"], request.json["email"])
    db.session.add (newUser)
    db.session.commit()
    return "user Successfull added\n\nTo login go to /login"

@app.route('/login', methods=['GET','POST'])
def login():
    username=request.json["username"]
    password=request.json["password"]
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(Users).filter(Users.username.in_([username]))
    result = query.first()
    hashed = Users.query().with_entities(Users.password)
    bool=check_password_hash(hashed,password)
    if result and bool:
        session['logged_in'] = True
        session['username']=username
        return home()
    else:
        return "Wrong password "+ password


@app.route('/logout', methods=['GET','POST'])
def logout():
    session['logged_in'] = False
    return home()

if __name__=="__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
