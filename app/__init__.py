# import packages
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

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

# the app object imports a routes object, models defines the structure of the sqlite database.
from app import routes, models, errors
