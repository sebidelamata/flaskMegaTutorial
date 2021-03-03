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
    # find mail server variables if they are set in the environment
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # email is on default 25 unless otherwise stated
    MAIL_PORT = os.environ.get('MAIL_PORT') or 25
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # these people will receive error logs
    ADMINS = ['sebidelamata@gmail.com']
    # this defines our posts per page
    POSTS_PER_PAGE = 4
