from . import db                                                                # The . implies import from __inti__.py
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from . import db


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16


# Create database table
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')             # The 'many' side of the relationship to User

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm


    def __repr__(self):
        # return '<Role %r>' % self.name                                        # Python 2 syntax
        return repr('Role ' + self.name)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))                  # Create the 'One' side of the relationship to role
    confirmed = db.Column(db.Boolean, default=False)                            # For User Authentication

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')            # set password to Write-only property
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def generate_confirmation_token(self, expiration=3600):
        """
        Generates a token with a default validity time of 1 hour
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')


    def confirm(self, token):
        """
        If valid, sets the new confirmed attribute in the user model to True
        Also checks that the id from the token matches the logged-in user, which
        is stored in current_user. This ensures that a confirmation token for a 
        given user cannot be used to confirm a different user.
        """
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True


    def __repr__(self):
        # return '<User %r>' % self.username                                    # python 2 syntax
        return repr('User ' + self.username)


# User loader function for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
