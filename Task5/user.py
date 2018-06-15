from flask import Flask, json, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
import os
from flask_session import Session
from passlib.hash import sha256_crypt

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "UserData.db"))
app.config['SQLALCHEMY_DATABASE_URI']= database_file

sess=Session()
db = SQLAlchemy(app)

class User(db.Model):
	username=db.Column(db.String(80), primary_key=True)
	password=db.Column(db.String(80))

	def __init__(self, username, password):
		self.username = username
		self.password = sha256_crypt.encrypt(password)


@app.route("/")
def hello():
	return "Register here: /register \nLogin here: /login \n"

@app.route("/register", methods = ["GET", "POST"])
def register ():
	dataget=request.get_json(force=True)
	usr=User(dataget["username"], dataget["password"])
	db.session.add (usr)
	db.session.commit ()
	return jsonify ("You have been registered!")

@app.route("/login", methods= ["GET","POST"])
def login():
	if 'username' in session:
		return (session['username']+" is already logged in!")
	dataget=request.get_json(force=True)
	usr=User.query.filter_by(username = dataget["username"]).first()
	pwd = dataget["password"]
	if sha256_crypt.verify(pwd, usr.password):
		session['username']=usr.username
		return "Logged in! You can now visit /authorized"
	else:
		return jsonify({'Login':'False'})


@app.route("/authorized", methods = ["GET"])
def authorized():
	if 'username' in session: 
		return "Logged in as "+str(session['username'])
	else:
		return "NOT AUTHORIZED" 


@app.route("/logout", methods = ["GET"])
def logout ():
	if 'username' in session:
		session.pop('username', None)
		return "You have been logged out!"
	else:
		return "Not logged in!"

if __name__=="__main__":
	app.secret_key = os.urandom(24)
	app.config['SESSION_TYPE'] = 'filesystem'
	sess.init_app(app)
	app.debug = True
	app.run()



