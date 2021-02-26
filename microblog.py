# import modules
from app import app, db
from app.models import User, Post

# this adds the database and models insto the shell session
# the wrapper specifies that this function is a shell context function
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}
