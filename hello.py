import re
from flask import Flask, make_response, abort

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



"""
Create application name - Web server will pass all request to this object via WSGI
The only requried argument is the name of the main module or package of the application.
Flask use this argument '__name__' to determine the location fo the application, which in turn
allow it to locate other files that are part of the application.
"""
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')                         # Create database connection

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False                             # Use less memory

db = SQLAlchemy(app)                                                            # load an instance of the database


# create a migration instance
migrate = Migrate(app, db)


# Integration with Python Shell
@app.shell_context_processor                                                    # Add wrapped function to the shell context
def make_shell_context():
    return dict(db=db, User=User, Role=Role)                                    # Shell will import these items automatically into shell, 
                                                                                # in addition to app, which is imprted by default

@app.route('/')
def index():
    return '<h1>Hello Word!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, {}!</h1>'.format(name)

@app.route('/test')
def test():
    return '<h1>Bad Request</h1>', 400

# Create a response object using make_response
@app.route('/resObj')
def res_object():
    response = make_response('<h1>This document carries a cookie</h1>')
    response.set_cookie('answer', '42')
    return response

# Abort object
@app.route('/user/<int:id>')
def get_user(id):
    user = None
    if not user:
        abort(404)
    return '<h1>XXX, {}</h1>'.format(user.name)


# Create database table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')             # The 'many' side of the relationship to User

    def __repr__(self):
        # return '<Role %r>' % self.name                                        # Python 2 syntax
        return repr('Role ' + self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))                  # Create the 'One' side of the relationship to role

    def __repr__(self):
        # return '<User %r>' % self.username                                    # python 2 syntax
        return repr('User ' + self.username)


