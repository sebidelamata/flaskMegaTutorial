from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

# Homepage
@app.route('/')
# aka index page
@app.route('/index')
#login is required to see this page
@login_required
def index():
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
    return render_template('index.html', title='Home', posts=posts)

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
        # else login the user and remember their authentication deets
        login_user(user, remember=form.remember_me.data)
        # 'next' is added to the url string
        next_page = request.args.get('next')
        # if the url does not have a next argument,
        # next page is set to the home page the user is redirected to their home page
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        # else redirect the user to the page they wanted to go to
        return redirect(next_page)
    # return the login page template to the user
    return render_template('login.html', title='Log in', form=form)

# this function allows users to logout
# this decorator function declares the view route
@app.route('/logout')
# logout logs the user out then redirects them to the index view
def logout():
    logout_user()
    return redirect(url_for('index'))

# this view function allows users to register for an account
# this wrapper function declares the path for the view,
# as well as invoking the get and post methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if the user is already logged in and tries to register send
    # them to their homepage bc they dont need to be here
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # form is an instance of a registration form
    form = RegistrationForm()
    # if the form goes through validly (is that a word?)
    # set their password to what they entered in the form,
    # add the user with all the fields (except user id)
    # then commit the add to the database,
    # then flash a message letting them know and redirect them to the login page
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been registered!, Login to start!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# this function creates a user profile view at user slash
# then whatever the username is. Login is required to be at this page
@app.route('/user/<username>')
@login_required
def user(username):
    # try to load the user from the database or go to a 404 error
    user = User.query.filter_by(username=username).first_or_404()
    # this is a list of test posts
    posts = [
        {'author': user, 'body': "Test post #1"},
        {'author': user, 'body': "Test post #2"}
    ]
    return render_template('user.html', user=user, posts=posts)
