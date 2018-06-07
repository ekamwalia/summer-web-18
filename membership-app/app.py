from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

project_dir = os.path.abspath(os.path.dirname(__file__))
db_file = "sqlite:///" + (os.path.join(project_dir, "memberdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)

class Members(db.Model):
	reg = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	contact = db.Column(db.String(100), nullable = False)

	def __init__(self, reg, name, contact):
		db.create_all()
		self.reg = reg
		self.name = name
		self.contact = contact

@app.route('/add', methods = ["POST"])
def add():
	data = request.get_json()
	if 'reg' not in data:
		abort(400)
	new_member = Members(data.get('reg'), data.get('name'), data.get('contact'))
	db.session.add(new_member)
	db.session.commit() 
	return "Added " + str(new_member.reg)

@app.route('/get', methods = ["GET"])
def get():
	members = []
	for m in Members.query.all():
		members.append({"reg" : m.reg, "name" : m.name, "contact" : m.contact})
	return jsonify(members)

@app.route('/update/<reg>', methods = ["PUT"])
def update(reg):
	member = Members.query.get(reg)
	if member is None:
		abort(400)

	data = request.get_json()
	member.reg = data.get('reg')
	member.name = data.get('name')
	member.contact = data.get('contact')

	db.session.commit()
	updated_member = {"reg" : member.reg, "name" : member.name, "contact" : member.contact}
	return jsonify(updated_member)

@app.route('/delete/<reg>', methods = ["DELETE"])
def delete(reg):
	member = Members.query.get(reg)
	if member is None:
		abort(400)
		
	db.session.delete(member)
	db.session.commit()
	return "Deleted " + str(member.reg)

if __name__ == "__main__":
	app.run(debug = True)