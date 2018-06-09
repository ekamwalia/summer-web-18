from flask import Flask, session, jsonify, request, redirect, url_for, escape
from flask_session import Session
import os
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt


project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "cruddb.db"))
app=Flask (__name__)
sess=Session()
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class Users (db.Model):
    username=db.Column (db.String (80), primary_key='True')
    password=db.Column(db.String (80))

    def __init__ (self, username, password):
        self.username=username
        self.password=sha256_crypt.encrypt (password)

@app.route ('/register', methods=['GET', 'POST'])
def register ():
    data=request.json
    user=Users (data ['username'], data['password'])
    db.session.add (user)
    db.session.commit ()
    return jsonify (data)

@app.route ("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return (session['username'] + " is logged in")
    data=request.json 
    user=Users.query.filter_by (username=data['username']).first ()
    if sha256_crypt.verify (data['password'], user.password):
        #login successful 
        session['username']=data['username'] #set session variable
        return redirect(url_for ('index'))
    else:
        return jsonify({'Login': 'False'})

@app.route ("/index", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return 'You are logged in as %s' % escape (session['username'])
    return 'You are not logged in.'

@app.route ("/logout",methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop ('username', None)
        return 'You are logged out'  
    else:
        return ('You were never logged in')   

if (__name__=="__main__"):
    app.secret_key =os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()