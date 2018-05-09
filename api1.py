from flask import Flask, jsonify, request, json
import random
app = Flask(__name__)

quotes = ["uno", "dos", "tres", "cuantro", "cinco"]

@app.route("/")
def intro():
	return '1. Add a new quote(/add) 2. Get a random​ quote(/random1) 3. Get all available quotes.(/all)'

@app.route("/add", methods=["POST"])
def add():
	q = request.json['quotes']
	quotes.append(q)
	return 'Quote added'
	
@app.route("/random1", methods=['GET'])
def random_quote():
	return jsonify(quotes[random.randrange(len(quotes))])
	
@app.route("/all", methods=['GET'])
def print_all():
	return jsonify(quotes)