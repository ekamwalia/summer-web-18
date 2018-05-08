from flask import Flask,request,jsonify,json
import random
app=Flask(__name__)

a=["i am a god","im not a god","im shit","inspirational my fucking ass","boooooooom"]


@app.route('/')
def index():

    return 'do you want to 1)see all the quotes 2)select a random quote 3)add a new quote '

@app.route('/allquotes',methods=['POST','GET'])
def bs():
    return jsonify(a)

@app.route('/random',methods=['POST','GET'])
def random():

     return jsonify(random.choice(a))

@app.route("/addQuote", methods = ["POST"])
def add_quote() :
	json_data = request.json

	a.append(json_data['a'])

	return "Quote added"

if  __name__=='__main__':
   app.debug=True
   app.run()
