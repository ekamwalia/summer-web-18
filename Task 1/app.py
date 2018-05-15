from flask import Flask, json, request
from random import  randint
app=Flask(__name__)

quoteList=["dAzEd aNd ConFuseD", "cOmFortBly nUMb","sMeLLs lIke TeEn sPirIt", "whO tOuChed mY sPaGHETT"]

@app.route("/")
def hello():
    return "Add quote: /add \n Random quote: /random \n Display all: /all"

@app.route("/add", methods=['GET', 'POST'])
def add():
    quoteList.append(request.get_json(["quote"]))
    return "Quote added!"
@app.route("/random")
def random():
    return json.dumps(quoteList[randint(0,len(quoteList)-1)])
@app.route("/all")
def all():
    return json.dumps(quoteList)

if __name__=="__main__":
    app.run()



