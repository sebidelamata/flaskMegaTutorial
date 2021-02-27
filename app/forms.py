# python treats forms like classes
# luckily we have a bunch of premade classes
# that help make designing a form much quicker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
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
