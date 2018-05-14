# from app import app

from flask import Flask,request,jsonify,json

app = Flask(__name__)

from random import randint

quotes = [ "'If people do not believe that mathematics is simple, it is only because they do not realize how complicated life is.' -- John Louis von Neumann ",
               "'Computer science is no more about computers than astronomy is about telescopes' --  Edsger Dijkstra ",
               "'To understand recursion you must first understand recursion..' -- Unknown",
               "'You look at things that are and ask, why? I dream of things that never were and ask, why not?' -- Unknown",
               "'Mathematics is the key and door to the sciences.' -- Galileo Galilei",
               "'Not everyone will understand your journey. Thats fine. Its not their journey to make sense of. Its yours.' -- Unknown"  ]

@app.route('/')
@app.route('/index')
def index():
  return "1. Add new quote (/add)\n2. Get random quote (/getrandom)\n3. Get all available quotes (/all)\n"

@app.route('/add', methods=['POST'])
def add():

  q=request.json['quotes']
  quotes.append(q)
  return "\nsuccess\n"

@app.route('/getrandom',methods=['GET'])
def getRandom():  
  randomNumber = randint(0,len(quotes)-1) 
  Quote = quotes[randomNumber] 
  return jsonify(Quote)

@app.route('/all', methods=['GET'])
def getAll():
  return jsonify(quotes)