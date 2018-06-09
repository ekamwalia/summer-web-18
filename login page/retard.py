from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:anmolrox@localhost/contacts'
db = SQLAlchemy(app)

class Example(db.Model):
	__tablename__ = 'login'
	username  = db.Column('username', db.Unicode,primary_key=True)
	password= db.Column('password', db.Unicode)

	def __init__(self,username,password):
		self.username=username
		self.password=password
