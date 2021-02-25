from flask import render_template
from app import app

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
    return render_template('index.html', user=user, post=posts)
