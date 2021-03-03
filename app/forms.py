# python treats forms like classes
# luckily we have a bunch of premade classes
# that help make designing a form much quicker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

# here is our login for class that requires a user to enter
# in values for their username, password, and they can
# optionally stay logged in, then the button to submit the info
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# this is our registration form class so that users can register for an account
class RegistrationForm(FlaskForm):
    # username is a required argument
    username = StringField('Username', validators=[DataRequired()])
    # so is email, and it also has to be a valid email  address
    email = StringField('Email', validators=[DataRequired(), Email()])
    # password is required
    password = PasswordField('Password', validators=[DataRequired()])
    # so is password2, and it must be the same as what they
    # filled in in the first password field
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    # finally a submit button
    submit = SubmitField('Register')

    # this function validates that the username has not already been used
    def validate_username(self, username):
        # first is queries for usernames that match the one entered on the registration form
        user = User.query.filter_by(username=username.data).first()
        # if there are any matches raise an error
        if user is not None:
            raise ValidationError('This username has already been taken, try another.')

    def validate_email(self, email):
        # first we query for emails that match the one entered in the registration form
        email = User.query.filter_by(email=email.data).first()
        # if there are any matches raise an error
        if email is not None:
            raise ValidationError('There is already an account associated with this email')

# this form allows users to edit their profile infor
class EditProfileForm(FlaskForm):
    # it requires a username
    username = StringField('Username', validators=[DataRequired()])
    # an optional about me field can have up to 500 characters
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=500)])
    # and a submit button
    submit = SubmitField('Submit')

    # this initializes the old username as a variable that can be looked up later
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    # this takes the username argument and if it is not the same as the
    # original username variable created in the __init__ function,
    # then we query our database to check if this name already exists (doesnt not exist)
    # if it doesnt not exist then we raise them an error and ask them to enter a unique username
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data). first()
            if user is not None:
                raise ValidationError('This username has already been taken, please enter a new one.')

# this is just an empty form with a submit button
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

# this form allows users to make posts
class PostForm(FlaskForm):
    # this is a text field that allows the user to post up to 500 characters
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=500)])
    # this allows the user to submit the form
    submit = SubmitField('Submit')
