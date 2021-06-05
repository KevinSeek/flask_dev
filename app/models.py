from . import db                                                                # The . implies import from __inti__.py
from werkzeug.security import generate_password_hash, check_password_hash


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
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')            # set password to Write-only property
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        # return '<User %r>' % self.username                                    # python 2 syntax
        return repr('User ' + self.username)