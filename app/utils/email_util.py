# import smtplib
# from email.mime.text import MIMEText

# def send_email(to_email: str, subject: str, body: str):
#     msg = MIMEText(body, "html")
#     msg["Subject"] = subject
#     msg["From"] = "no-reply@example.com"
#     msg["To"] = to_email

#     with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
#         server.login("mtm.linnaunghtet@gmail.com", "yfqg uhmj hezo ptdx")
#         server.send_message(msg)


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

