from app.extension import mail
from flask_mail import Message

def send_email(to_email: str, subject: str, body: str, html: str | None = None):
    msg = Message(
        subject=subject,
        recipients=[to_email],
    )
    msg.body = body
    if html:
        msg.html = html
    mail.send(msg)

