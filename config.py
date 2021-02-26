# Secret key configuration
import os

# define our base directory
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # this variable is the user's secret key or the hardcoded backup string
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # this variable establishes the path and name for the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # we do not need to signal the app everytime a change is made to the database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
