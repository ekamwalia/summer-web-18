from flask import Flask, jsonify
import json
from flask import request
from random import randint
app = Flask(__name__)

qoute = ["q1","q2","q3","q4"]

@app.route('/')
def intro():
    return 'Welcome to this page please enter a preffered choice 1)generate a random qoute,2)add a qoute,3)show all the qoutes'

@app.route('/hello')
def hello():
	return 'HELLO WORLD!!'

@app.route('/allqoutes',methods=['GET'])
def all_qoutes():
	return jsonify(qoute)


@app.route('/randqoute',methods=['GET'])
def rand_qoutes():
	a=randint(0,3)
	return jsonify(qoute[a])

@app.route('/addnew',methods=['POST'])
def new():
	data=request.get_json(force=True)
	qoute.append(data)
        return jsonify({'quote added':data})

