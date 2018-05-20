from flask import Flask
hello1 = Flask(__name__)

@hello1.route('/')
def index():
    return 'Hello World'

if __name__ == '__main__':
    hello1.run(debug=True)
