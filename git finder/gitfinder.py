from flask import Flask, render_template, request
import requests
d=[]
app = Flask(__name__)
username=None
@app.route('/details', methods=['POST'])
def details():
    global username,d

    username = request.form['username']
    d=[]
    r = requests.get('https://api.github.com/users/'+username+'')
    json_object = r.json()
    name = str(json_object['name'])
    email=str(json_object['email'])
    location=str(json_object['location'])
    company=str(json_object['company'])
    followers=str(json_object['followers'])
    following=str(json_object['following'])
    hireable=str(json_object['hireable'])
    return render_template('profile.html',name=name,email=email,location=location,company=company,followers=followers,following=following,hireable=hireable)

@app.route('/repos')
def repos():
    global username,d
    d=[]
    a = requests.get('https://api.github.com/users/'+username+'/repos')
    json=a.json()
    for i in json:
        d.append(str(i['name']))
    return str(d)
@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
