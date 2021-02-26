# python treats forms like classes
# luckily we have a bunch of premade classes
# that help make designing a form much quicker
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

# here is our login for class that requires a user to enter
# in values for their username, password, and they can
# optionally stay logged in, then the button to submit the info
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')
