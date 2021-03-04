from flask_mail import Message
from app import mail, app
from flask import render_template
from threading import Thread

def send_async_email(app, msg):
    with app.context():
        mail.send(msg)

# here we assign fields for our message and send it through asynchronous enail
def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject,
                  sender=sender,
                  recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(app, msg)).start()

# here we create a password reset token and send an email
# using the function we created above
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[Microblog] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user,
                                         token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user,
                                         token=token)
               )
