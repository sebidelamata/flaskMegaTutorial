# import packages
from flask import render_template
from app import app, db

# this function returns a custom html for 404 errors as well as a 404 status
# the decorator function registers this for error 404 with flask
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# this function returns a custom html and attempts to rollback the server
# to the last recoverable state in the event of a 500 error
# this decorator functio registers this for 500 errors with flask
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
