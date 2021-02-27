from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User

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
# The wrapper function invokes both the get in post methods to
# receive the form and output to the desired landing page
@app.route('/login', methods=['GET', 'POST'])
def login():
    # this first checks if the user has been authenticated, and if they have,
    # then they are passed to their home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # create a variable form that is an instance of the login form class
    form = LoginForm()
    # if the form is not validated on submission the user is
    # warned and sent back to the login page
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # the flash function with flash the dialogue to the user
        return redirect(url_for('/index'))
    # return the login page template to the user
    return render_template('login.html', title='Log in', form=form)
