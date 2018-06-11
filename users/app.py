from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

project_dir = os.path.abspath(os.path.dirname(__file__))
db_file = "sqlite:///" + (os.path.join(project_dir, "userdb.db"))

app = Flask(__name__)
app.config["SQL_DATABASE_URI"] = db_file
app.config["SECRET_KEY"] = os.urandom(10)

db = SQLAlchemy(app)
login = LoginManager(app)

class Users(db.Model):
	userid = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(50), nullable = False, unique = True)
	password_hash = db.Column(db.String(128), nullable = False)
			
	def checkpassword(self, password):
		return check_password_hash(self.password_hash, password)

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.userid)

	def __init__(self, username, password):
		self.username = username
		self.password_hash = generate_password_hash(password)

db.create_all()


@login.user_loader
def load_user(id):
	return Users.query.get(int(id))

@app.route('/protected')
@login_required
def logged_in():
	return "Logged in"

@app.route('/register', methods = ['POST'])
def adduser():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')
	if Users.query.filter_by(username = username).first():
		return "Username exists"
	else:
		new_user = Users(username, password)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user)
		return redirect(url_for('logged_in'))

@app.route('/login', methods = ['POST'])
def login():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')
	user = Users.query.filter_by(username = username).first()
	if user is None or not user.checkpassword(password):
		return "Invalid username or password"
	else:
		login_user(user)
		return redirect(url_for('logged_in'))

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return "Logged out"

if __name__ == '__main__':
	app.run(debug = True)



	


