from flask import Flask, jsonify, request
from random import choice

# Initialize flask object
app = Flask(__name__)

# Global array for storing all quotes
all_qoutes = ['Quote 1', 'Quote 2', 'Qoute 3']


# Index route
@app.route('/')
@app.route('/hello')
def hello():

	resp = {}
	resp['success'] = True
	resp['message'] = "Welcome to Random Quote Generator API"
	resp['data'] = None

	return jsonify(resp), 200


# Show all qoutes
@app.route("/allQuotes")
def all():

	resp = {}
	resp['success'] = True
	resp['message'] = "Found: " + str(len(all_qoutes)) +" qoutes."
	resp['data'] = all_qoutes

	return jsonify(resp), 200


# Show a random qoutes
@app.route("/randomQuote")
def random():

	resp = {}
	resp['success'] = True
	resp['message'] = None
	resp['data'] = choice(all_qoutes)

	return jsonify(resp), 200


# Add new quote
@app.route("/addQuote", methods=['POST'])
def add():

	req_data = request.get_json(silent=True)

	if req_data is None:
		resp = {}
		resp['success'] = False
		resp['message'] = "JSON Data not POSTed"
		resp['data'] = None

		return jsonify(resp), 400

	if req_data.get('quote') is None:
		resp = {}
		resp['success'] = False
		resp['message'] = "'quote' field not found in request"
		resp['data'] = None

		return jsonify(resp), 400

	all_qoutes.append(req_data['quote'])
	resp = {}
	resp['success'] = True
	resp['message'] = "New quote added"
	resp['data'] = all_qoutes

	return jsonify(resp), 201


if __name__ == "__main__":

	app.debug = True
	app.run()
