from flask import Flask,request,jsonify,json
import random
from flask_sqlalchemy import SQLAlchemy
from ghj import Example
from ghj import db
from random import randint
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:anmolrox@localhost/contacts'
db = SQLAlchemy(app)
a=[]
examples=Example.query.all()
for y in examples:
    a.append(y.quote)




@app.route('/')
def index():

    return 'do you want to 1)see all the quotes 2)select a random quote 3)add a new quote '

@app.route('/allquotes',methods=['POST','GET'])
def bs():
    examples=Example.query.all()

    return jsonify(a)

@app.route('/random',methods=['POST','GET'])
def random():

    one=Example.query.filter_by(rollno=randint(0,int(len(a)))).first()
    return one.quote



@app.route("/addQuote", methods = ["POST"])
def add_quote() :


 json_data = request.json
 new_ex=Example(int(len(a))+1,json_data['a'])
 db.session.add(new_ex)
 db.session.commit()



 return "Quote added"

if  __name__=='__main__':
   app.debug=True
   app.run()
