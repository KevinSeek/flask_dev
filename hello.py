from flask import Flask



"""
Create application name - Web server will pass all request to this object via WSGI
The only requried argument is the name of the main module or package of the application.
Flask use this argument '__name__' to determine the location fo the application, which in turn
allow it to locate other files that are part of the application.
"""

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello Word!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)
