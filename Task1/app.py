from flask import Flask, json, request
from random import randint
app=Flask(__name__)

quotes=["abc", "cde", "fgh"]

@app.route ("/")
def hello():
	return "Add a quote: /add \n Random Quote: /random \n All available quotes: /all"

@app.route ("/add", methods=['GET', 'POST'])
def add():
	quotes.append (request.get_json())
	return "Quote appended"

@app.route ("/random")
def random():
	return json.dumps (quotes[randint (0, len(quotes)-1)]);

@app.route ("/all")
def all():
	return json.dumps(quotes)


if __name__=="__main__":
	app.run()
