# import packages
from flask import Flask

# create application object consisting of a Flask instance
app = Flask(__name__)

# the app object imports a routes object, which doesnt exist yet.
from app import routes
