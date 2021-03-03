# import packages
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask_mail import Mail

# create application object consisting of a Flask instance
app = Flask(__name__)

# after we create the app object we tell the app to generate
# the secret key from the Config class in the config file
# to prevent CSRF attacks from our forms
app.config.from_object(Config)

# this db object represents the database
db = SQLAlchemy(app)

# this migrate object represents the data migration engine
migrate = Migrate(app, db)

# this login object is an instance of a LoginManager that
# allows users to stay logged in while they browse through different views
login = LoginManager(app)

# here we are telling flask-login which
# of our view functions handles the login
login.login_view = 'login'

# this is an instance of a mail service
mail = Mail(app)

# the app object imports a routes object,
# models defines the structure of the sqlite database.
# errors is for our custom error handling
from app import routes, models, errors

# this only runs when the app is not in debug mode
if not app.debug:
    # if the config file has a value for mail-server then auth is set to none
    if app.config['MAIL_SERVER']:
        auth = None
        # if there is a value for the mail username and password lets use those to authenticate
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        # secure is set to none
        secure = None
        # if the file has a value for MAIL use tls then secure is set to that value
        if app.config['MAIL_USE_TLS']:
            secure = ()
        # an instance of the smtp service is create with the variables plugged in
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'],
            subject='Microblog failure',
            credentials=auth, secure=secure
        )
        # the level is set to a logging error
        mail_handler.setLevel(logging.ERROR)

    # if there isn't already a subdirectory named logs, make one
    if not os.path.exists('logs'):
        os.mkdir('logs')
    # file handler is an instance of a RotatingFileHandler class
    # rotating logs makes sure we don't have a giant file when the
    # app have been running for awhile. We limit the size of the
    # logfile and only keep the last ten logfiles
    file_handler = RotatingFileHandler('logs/microblog.log',
                                       maxBytes=10240,
                                       backupCount=10)
    # a little formatting for our log messages
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
