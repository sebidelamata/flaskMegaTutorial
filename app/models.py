# import our database object
from app import db

class User(db.Model):
    # id column is an int primary key
    id = db.Column(db.Integer, primary_key=True)
    # can't have someone elses username
    username = db.Column(db.String(64), index=True, unique=True)
    # one email can not have multiple accounts
    email = db.Column(db.String(120), index=True, unique=True)
    # password hash is the encrypted password that is stored in the database
    # (not the actual password)
    password_hash = db.Column(db.String(128))

    # this method tells python how to print the objects in this
    # class instead of just returning the object
    def __repr__(self):
        return '<User {}>'.format(self.username)
