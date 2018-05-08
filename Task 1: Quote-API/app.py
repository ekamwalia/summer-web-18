from flask import Flask, request, jsonify
import random

app = Flask(__name__)

quotes = []

@app.route("/")
def index():
    return "Welcome to the Random Quote Generator API."

@app.route("/add", methods=["POST"])
def add_quote():
    if not request.json or not 'quote' in request.json:
        abort(400)
    quote = request.json['quote']
    quotes.append(quote)
    return jsonify({'quote': quote}), 201

@app.route("/random", methods=["GET"])
def get_random():
    if not quotes:
        return "No quotes found!", 404
    return jsonify({'quote': random.choice(quotes)})

@app.route("/all", methods=["GET"])
def get_all():
    if not quotes:
        return "No quotes found!", 404
    return jsonify({'quotes': quotes})

if __name__ == "__main__":
    app.run(debug=True)
