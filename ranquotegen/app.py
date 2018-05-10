from flask import Flask, request, jsonify
import json
import random
app = Flask(__name__)

quotes = ["plata o plomo","the game is on","friends don't lie","louis goddamn litt"]

@app.route('/')
def intro():
    return 'Welcome to quote generator. showall- show all present quotes. random- get a random quote. new-add a new quote.'


@app.route('/quotes/showall',methods=['GET'])
def all_quotes():
	return jsonify(quotes)

@app.route('/quotes/random',methods=['GET'])
def rand_quotes():
	return jsonify({'quote': random.choice(quotes)})

@app.route('/quotes/new', methods = ['POST'])
def add_quote() :
    if not request.json:
        abort(400)
    data = request.json['quote']
    quotes.append(data)
    return jsonify({'quote':data})



if __name__ == "__main__":
    app.run(debug=True)
