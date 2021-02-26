from flask import render_template
from app import app
from app.forms import LoginForm

# Homepage
@app.route('/')
@app.route('/index')
def index():
    # user is the account holder (you if you are using the page)
    user = {'username':'Sebi'}
    # posts is a list containing nested dictionaries (pretty much json)
    # that holds posts of users connected to the account of the current user (you)
    posts = [
        {
            'author': {'username': 'Jerry'},
            'body': 'My hair smells like old turkey and this upsets me.'
        },
        {
            'author': {'username': 'Joe'},
            'body': 'Bet no cap hunnid'
        }
    ]
    return render_template('index.html', user=user, posts=posts)

# This view function is for the login page
@app.route('/login')
def login():
    # create a variable form that is an instance of the login form class
    form = LoginForm()
    # return the login page template to the user
    return render_template('login.html', title='Log in', form=form)
