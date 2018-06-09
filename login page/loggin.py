from flask import Flask, session, render_template, request, redirect, g, url_for
import os
from flask import Flask,request,jsonify,json
import random
from flask_sqlalchemy import SQLAlchemy
from retard import Example
from retard import db
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:anmolrox@localhost/contacts'
db = SQLAlchemy(app)


app.secret_key = os.urandom(24)


@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':


     session.pop('user', None)

     json_data = request.json
     examples=Example.query.all()
     for ex in examples:
        if (str(ex.password)==str(json_data['password'])) & (str(ex.username)==str(json_data['username'])):
           session['user'] = str(json_data['username'])
           return redirect(url_for('protected'))

    return "enter valid username and password"
@app.route("/register", methods = ["POST"])
def register() :


 json_data = request.json
 new_ex=Example(json_data['username'],json_data['password'])
 db.session.add(new_ex)
 db.session.commit()
 return "registered"


@app.route('/protected')
def protected():
    if g.user:
        return "logged in"

    return  redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']


@app.route('/dropsession')
def dropsession():
    session.pop('user', None)
    return 'Dropped!'

if __name__ == '__main__':
    app.run(debug=True)
