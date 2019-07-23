import os 
from flask import Flask
app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, this is implication of yandex backend school's task by Evgeniy Khomutov"


@app.route('/imports',methods=['POST'])
def post():
    pass

@app.route('/PATCH')
def patch():
    pass

@app.route('/GET')
def get():
    pass

@app.route('/test_<name>')
def FUNCTION(name):
    return(name)

if __name__ == '__main__':
    app.run()