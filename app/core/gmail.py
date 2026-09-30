import base64
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.core import settings
from app.core.google_api import gmail_service
from app.core.settings import config
from smtplib import SMTP_SSL
import ssl


def send_email(subject, sender_name=config.sender_name, sender_email=config.sender_email, body_plain=None, body_html=None, recipients=None, filename=None, attachment=None):
    message = EmailMessage()

    # send both plain text and html email
    message.set_content(body_plain)
    message.add_alternative(body_html, subtype="html")

    if attachment:
        message.add_attachment(
            attachment, maintype="application", subtype="pdf", filename=f"{filename}.pdf")

    # create the email message, setting the subject, from, and to
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = ", ".join(recipients)

    # prepare the payload to the GMail API
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    gmail_body = {"raw": encoded_message}

    # send the email
    gmail_service.users().messages().send(userId="me", body=gmail_body).execute()


def send_email_pro(subject, sender_name=config.sender_name, sender_email=config.sender_email, body_plain=None, body_html=None, recipients=None, filename=None, attachment=None):
    message = EmailMessage()

    # send both plain text and html email
    message.set_content(body_plain)
    message.add_alternative(body_html, subtype="html")

    if attachment:
        message.add_attachment(
            attachment, maintype="application", subtype="pdf", filename=f"{filename}.pdf")

    # create the email message, setting the subject, from, and to
    message["Subject"] = subject
    message["From"] = f"{sender_name} <{sender_email}>"
    message["To"] = ", ".join(recipients)
    message["Reply-To"] = sender_email

    context = ssl.create_default_context()

    with SMTP_SSL(host=config.smtp_server, port=config.smtp_port, context=context) as server:
        server.login(user=config.smtp_user, password=config.smtp_password)
        server.send_message(msg=message)


def send_email_costum(to, plaintext, html, subject, sender_name=config.sender_name, sender_email=config.sender_email, attachment=None, filename=None):
    msg = MIMEMultipart('alternative')

    msg['To'] = to
    msg['Subject'] = subject
    msg['From'] = f"{sender_name} <{sender_email}>"
    text_part = MIMEText(plaintext, 'plain')
    html_part = MIMEText(html, 'html')

    msg.attach(text_part)
    msg.attach(html_part)
    if attachment:
        if filename is None:
            filename = "attachment"
        msg.add_attachment(
            attachment, maintype="application", subtype="pdf", filename=f"{filename}.pdf")

    context = ssl.create_default_context()

    with SMTP_SSL(host=config.smtp_server, port=config.smtp_port, context=context) as server:
        server.login(user=config.smtp_user, password=config.smtp_password)
        server.send_message(msg=msg)


if __name__ == "__main__":
    subject = "Test Email"
    sender_name = "PyCon Togo 2026 team"
    body_plain = "This is a test email sent from the Gmail API."
    body_html = "<p>This is a <strong>test email</strong> sent from the Gmail API.</p>"
    recipients = ["wasscodeur228@gmail.com"]

    send_email_pro(subject, body_plain=body_plain,
                   body_html=body_html, recipients=recipients)
