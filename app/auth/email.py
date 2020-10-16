from app.email import send_email
from flask import current_app, render_template

def send_password_reset(user):
    token = user.get_token()
    send_email('Resest password',
            sender=current_app.config['ADMINS'][0],
            recipients=[user.email],
            text_body= render_template('email/reset_password.txt',
                                        user = user, token = token),
            html_body= render_template('email/reset_password.html',
                                        user = user, token = token))