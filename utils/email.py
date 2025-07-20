from flask_mail import Message
from extensions import mail
from flask import current_app
import traceback

def send_inquiry_email(inquiry):
    print("send_inquiry_email called from:")
    traceback.print_stack()
    subject = "New Event Inquiry"
    print("EMAIL DEBUG: subject =", subject, "type =", type(subject))
    if not isinstance(subject, str):
        raise ValueError("Subject must be a string")
    sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    recipients = [current_app.config.get('MAIL_DEFAULT_SENDER')]
    reply_to = inquiry.email
    body = f"New inquiry from {inquiry.name} ({inquiry.email}):\n\n{inquiry.message}"
    print("Email subject:", type(subject), subject)
    print("Sender:", type(sender), sender)
    print("Recipients:", type(recipients), recipients)
    print("Reply-to:", type(reply_to), reply_to)
    print("Body:", type(body), body)
    msg = Message(
        subject=subject,
        sender=sender,
        recipients=recipients,  # Send to admin
        reply_to=reply_to,  # Set reply-to as the user's email
        body=body
    )
    mail.send(msg)
