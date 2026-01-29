from app.utils.email_util import send_email
from flask import render_template

def send_reset_password_email(email: str, reset_link: str):
    html = render_template(
        "mails/reset_password.html",
        reset_link=reset_link
    )
    text = render_template(
        "mails/reset_password.txt",
        reset_link=reset_link
    )

    send_email(
        email,
        "Reset Password",
        text,
        html
    )
