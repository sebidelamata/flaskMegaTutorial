# import our database object
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# users table
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
    # defines a relationship with post tab
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # this method tells python how to print the objects in this
    # class instead of just returning the object
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # this method sets the password hash value for a user to a
    # hash generated from the user's password input
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # this method checks the users registered password hash against
    # the one created by the user input for password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# posts table
class Post(db.Model):
    # post id is primary key int
    id = db.Column(db.Integer, primary_key=True)
    # body is the actual post that can be up to 500 characters
    body = db.Column(db.String(500))
    # timestamp is the time of the posting in UTC
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user id is the userid and is linked to the users table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # this method tells python how to print the objects in this
    # class instead of just returning the object
    def __repr__(self):
        return '<Post {}>'.format(self.body)
