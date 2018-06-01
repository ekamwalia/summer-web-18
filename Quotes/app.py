from flask import Flask, jsonify, request
import random

app = Flask(__name__)

quotes = ['quote1', 'quote2']

@app.route('/addquote', methods=['POST'])
def add_quote():
	new_quote = request.json['quote']
	quotes.append(new_quote)
	return jsonify({'quotes': quotes})

@app.route('/getquotes', methods=['GET'])
def get_quotes():
	return jsonify({'quotes': quotes})

@app.route('/randomquote', methods=['GET'])
def random_quote():
    return jsonify({'quotes': random.choice(quotes)})

if __name__=='__main__':
	app.run(debug = True)
