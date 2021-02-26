# import packages
from flask import Flask
from config import Config

# create application object consisting of a Flask instance
app = Flask(__name__)
# after we create the app object we tell the app to generate
# the secret key from the Config class in the config file
# to prevent CSRF attacks from our forms
app.config.from_object(Config)

# the app object imports a routes object, which doesnt exist yet.
from app import routes
