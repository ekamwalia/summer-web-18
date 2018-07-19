from flask import Flask, session, jsonify, request, redirect, url_for, escape,render_template
from flask_session import Session
import os
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
import requests


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
    status=''
    if request.method == 'POST':
        data=request.form
        #username=data['username']
        #password=data['password']
        user=Users (data ['username'], data['password'])
        try:
            db.session.add(user)
            db.session.commit()
            status = 'Success'
        except:
            status = 'This user is already registered'
        db.session.close()
    return render_template ('signup.html', status=status)
    
@app.route ("/signin", methods=['GET', 'POST'])
def signin():
    #if request.method == 'POST'
    if 'username' in session:
        return 'User is already signed in'
    if request.method == 'POST':
        data=request.form
        user=Users.query.filter_by (username=data['username']).first ()
        if sha256_crypt.verify (data['password'], user.password):
            #login successful 
            session['username']=data['username'] #set session variable
            return redirect(url_for ('homepage'))
    return render_template('signin.html')

@app.route ("/homepage", methods=['GET', 'POST'])
def homepage ():
    if 'username' not in session:
        return 'Access denied'
    if request.method=='POST':
        user=request.form['search']
        data=requests.get ('https://api.github.com/users/'+user +'/repos')
        if data.ok:
            details=data.json() #list
            repolist=[]
            for repo in details:
                repolist.append (repo['name'])
            return render_template('homepage.html', username=session['username'], details=repolist)
        else:
            return render_template('homepage.html', username=session['username'], status='User not found')

    return render_template('homepage.html', username=session['username'])

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

@app.route ("/signout",methods=['GET', 'POST'])
def signout():
    if 'username' in session:
        session.pop ('username', None)
        return 'You have been signed out'  
    else:
        return ('You were never logged in')   

if (__name__=="__main__"):
    app.secret_key =os.urandom(12)
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)
    app.debug = True
    app.run()
