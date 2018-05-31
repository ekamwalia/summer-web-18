from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:anmolrox@localhost/contacts'
db = SQLAlchemy(app)

class Example(db.Model):
	__tablename__ = 'quote'
	rollno  = db.Column('rollno', db.Integer,primary_key=True)
	quote = db.Column('quote', db.Unicode)

	def __init__(self,rollno,quote):
		self.rollno=rollno
		self.quote=quote
