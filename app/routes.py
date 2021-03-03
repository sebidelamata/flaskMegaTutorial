from datetime import datetime
from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, EmptyForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post

# this function executes before any request
# and grabs the time to show the last time the user was seen
# the decorator function is from Flask and registers this
# function as something that needs to happen before the requests occur
@app.before_request
def before_request():
    # if the user is signed in then last seen is updated to right now
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        # commit this to the database
        db.session.commit()

# Homepage
@app.route('/', methods=['GET', 'POST'])
# aka index page
@app.route('/index', methods=['GET', 'POST'])
#login is required to see this page
@login_required
def index():
    # posts is a list containing nested dictionaries (pretty much json)
    # that holds posts of users connected to the account of the current user (you)
    # an object of an instance of our post form
    form = PostForm()
    # if the form is correctly submitted
    if form.validate_on_submit():
        # we create an instance of our Post containing the body of our post form
        post = Post(body=form.post.data, author=current_user)
        # add this post to our data base and flash a message
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    # posts is all the posts authored by the people the user follows,
    # this is paginated to the number of posts per page specified in the
    # config file
    posts = current_user.followed_posts()\
        .paginate(page,
                  app.config['POSTS_PER_PAGE'],
                  False)

    return render_template('index.html', title='Home', form=form, posts=posts.items)

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
    # we are instantiating the EmptyForm for follow/unfollow function here
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

# this view allows the user to edit their profile info
# this decorator function declares the route for the view
@app.route('/edit_profile', methods=['GET', 'POST'])
# the user must be signed in to see this view
@login_required
def edit_profile():
    # form is an instance of the EditProfileForm class we created in forms.py
    # this takes the arg current_user.username to check if the person editing
    # their profile has tried to change their username
    form = EditProfileForm(current_user.username)
    # if the user correctly fills in the form and submits it the values will be updated in the database
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    # otherwise thesed fields will be filled in with the most current values for this
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# this view allows the user to follow another user
# this decorator declares the route as well as the post method
@app.route('/follow/<username>', methods=['POST'])
# the user must be logged in to perform this
@login_required
def follow(username):
    # we have an empty for with a button
    form = EmptyForm()
    # if the user clicks the button we will try to follow
    if form.validate_on_submit():
        # user is the person we are trying to follow
        user = User.query.filter_by(username=username).first()
        # if that person is not in the database for some reason,
        # tell the user they couldnt find them and take them back tot the home page
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        # if the person is the user (they are trying to follow themselves)
        # tell them no and direct them to their profile page
        if user == current_user:
            flash('You can not follow yourself!')
            return redirect(url_for('user', username=username))
        # if those weird cases werent met then follow the person and commit it to the database
        current_user.follow(user)
        db.session.commit()
        flash('You are now following {}!'.format(username))
        return redirect(url_for('index'))

# the unfollow does the opposite of the view above
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found').format(username)
            return redirect(url_for('index'))
        if user == current_user:
            flash('You can not unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

# this view allows our users to explore other profiles that they are not currently connected to
# this decorator function establishes the route for the view
@app.route('/explore')
# the user must be logged in to view this view
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    # posts is all the posts in the dc in descending order by time
    posts = Post.query.order_by(Post.timestamp.desc())\
        .paginate(page, app.config['POSTS_PER_PAGE'], False)
    return render_template('index.html', title='Explore', posts=posts.items)
