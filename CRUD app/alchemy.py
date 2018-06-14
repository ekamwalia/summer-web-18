
from flask import Flask, jsonify, request, json
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
import os

app = Flask(__name__)

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "basicCRUD.db"))

app.config['SQLALCHEMY_DATABASE_URI']= database_file
db = SQLAlchemy(app)

class quotey(db.Model):
	quote_no = db.Column(db.Integer, primary_key = True)
	quote_data = db.Column(db.String, nullable = False)

	def __init__(self, quote_no, quote_data):
		self.quote_no = quote_no
		self.quote_data = quote_data

@app.route ("/")
def home ():
	return "Create, read, update, delete QuoTeS"

@app.route ("/create", methods = ["GET","POST"])
def create ():
	dataget=request.get_json(force=True)
	qno=dataget["quote_no"]
	qdta= dataget["quote_data"]
	quote=quotey(qno, qdta)
	db.session.add (quote)
	db.session.commit ()
	return "Added "+str(quote.quote_data)


@app.route ("/read", methods=['GET', 'POST'])
def read ():
	quote_list=[];
	quotes=quotey.query.order_by('quotey.quote_no').all()
	for n in quotes:
		quote_list.append(n.quote_data)
	return jsonify (quote_list)


@app.route("/update", methods=["GET", "POST"])
def update ():
	updateinfo=request.get_json(force=True)
	newquote = updateinfo["newquote"]
	oldquote = updateinfo["oldquote"]
	quote=quotey.query.filter_by(quote_data = oldquote).first()
	if quote is None:
		return "Quote doesn't exist"
	quote.quote_data=newquote
	db.session.commit ()
	return ("Updated "+oldquote+" to "+newquote)


@app.route("/delete", methods = ["GET","POST"])
def delete ():
	delinfo = request.get_json(force=True)["quote_no"]
	quote=quotey.query.filter_by(quote_no=delinfo).first()
	deldata = quote.quote_data
	if quote is None:
		return "Quote doesn't exist"
	db.session.delete(quote)
	db.session.commit()
	return "Deleted "+deldata

if __name__=="__main__":
	app.run(debug=True)