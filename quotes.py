from flask import *
from flask import jsonify#json
import random
import os
app=Flask(__name__)

all_quotes=["abcd efgh ijkl", "qwrt oiuy prut", "zxc cvb mnbc"]
@app.route("/")

def main():
	return "/all for all the quotes /random for random quote /addQuote for adding a quote"

@app.route("/all", methods=['POST', 'GET'])
def all():
	return jsonify(all_quotes)

@app.route("/random",methods=['POST','GET'])
def randomq():
	quote=all_quotes[random.randint(0,len(all_quotes)-1)]
	return jsonify(quote)

@app.route("/addQuote",methods=['GET','POST'])
def addQuote():
	request_json=request.get_json()
	newq=request_json.get("Enter quote")
	jsonify(all_quotes.append(newq))
	#new_quote = request.json['quote']
	#return jsonify(quotes.append(new_quote))
	#return str("quote added")
	#all_quotes.append(request.get_json()["quote"])
	#jsonify(all_quotes)
	return "quote added"

#main()
if __name__=="__main__":
	app.run(debug=True)

	

	#return jsonify(quote)#json.dump(quote)
