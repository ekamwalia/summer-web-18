from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

project_dir = os.path.abspath(os.path.dirname(__file__))
db_file = "sqlite:///" + (os.path.join(project_dir, "memberdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = db_file

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Members(db.Model):
	reg = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100), nullable = False)
	contact = db.Column(db.String(100), nullable = False)

	def __init__(self, reg, name, contact):
		db.create_all()
		self.reg = reg
		self.name = name
		self.contact = contact

class MemberSchema(ma.Schema):
	class Meta:
		fields = ('reg', 'name', 'contact')

member_schema = MemberSchema()
members_schema = MemberSchema(many = True)


@app.route('/add', methods = ["POST"])
def add():
	new_member = Members(request.json["reg"], request.json["name"], request.json["contact"])
	db.session.add(new_member)
	db.session.commit() 
	return member_schema.jsonify(new_member)

@app.route('/get', methods = ["GET"])
def get():
	all_members = Members.query.all()
	result = members_schema.dump(all_members)
	return jsonify(result.data)

@app.route('/update/<reg>', methods = ["PUT"])
def update(reg):
	member = Members.query.get(reg)
	reg = request.json["reg"]
	name = request.json["name"]
	contact = request.json["contact"]

	member.reg = reg
	member.name = name
	member.contact = contact

	db.session.commit()
	return member_schema.jsonify(member)

@app.route('/delete/<reg>', methods = ["DELETE"])
def delete(reg):
	member = Members.query.get(reg)
	db.session.delete(member)
	db.session.commit()
	return member_schema.jsonify(member)


if __name__ == "__main__":
	app.run(debug = True)