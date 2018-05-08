from flask import Flask
from flask import jsonify, request
import json
from random import randint
task1=Flask(__name__)
quote=[]

@task1.route('/')
def intro():
    return 'Welcome to quote'

@task1.route('/addquotes',methods=["POST"])
def add():
    new=request.json[quote]
    quote.append(new)
    return jsonify({'New quote added':new})

@task1.route('/randomquote',methods=["GET"])
def call():
    return jsonify({'random quote':random.choice(quote)})

@task1.route('/showquotes',methods=["GET"])
def quotes():
    return jsonify(quote)

if __name__ == "__main__":
    task1.run(debug=True)
