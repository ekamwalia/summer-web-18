from flask import Flask, session, jsonify, request, redirect, url_for, escape,render_template
from flask_session import Session
import os
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt


project_dir=os.path.dirname(os.path.abspath(__file__))
database_file="sqlite:///{}".format(os.path.join(project_dir, "appdb.db"))
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
    if request.method == 'POST':
        data=request.form
        #username=data['username']
        #password=data['password']
    
    user=Users (data ['username'], data['password'])
    db.session.add (user)
    db.session.commit ()
    return render_template ('signup.html')
    
@app.route ("/signin", methods=['GET', 'POST'])
def signin():
    #if request.method == 'POST':
    if request.method == 'POST':
        data=request.form
    user=Users.query.filter_by (username=data['username']).first ()
    if sha256_crypt.verify (data['password'], user.password):
        #login successful 
        session['username']=data['username'] #set session variable
        return redirect(url_for ('index'))
    return render_template('signin.html')


'''
@app.route ("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return (session['username'] + " is logged in")
    #render_template ('signin.html')
    data=request.form
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
    '''

@app.route("/index", methods=['GET', 'POST'])
def index ():
    return 'hi there'

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
