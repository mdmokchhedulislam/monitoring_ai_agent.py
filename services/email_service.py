
import os
import smtplib

from dotenv import load_dotenv
from email.message import EmailMessage

load_dotenv()


def send_email(subject: str, body: str, html_body: str = None):

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("APPROVAL_EMAIL")

    if not all([smtp_host, smtp_user, smtp_password, recipient]):
        raise ValueError("SMTP configuration is incomplete")

    message = EmailMessage()

    message["From"] = smtp_user
    message["To"] = recipient
    message["Subject"] = subject

    message.set_content(body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(message)

    print("Email sent successfully!")

























# import os
# import smtplib

# from dotenv import load_dotenv
# from email.message import EmailMessage


# # Load environment variables from .env
# load_dotenv()


# def send_email(subject: str, body: str):

#     # Read SMTP configuration
#     smtp_host = os.getenv("SMTP_HOST")
#     smtp_port = int(os.getenv("SMTP_PORT", "587"))
#     smtp_user = os.getenv("SMTP_USER")
#     smtp_password = os.getenv("SMTP_PASSWORD")
#     recipient = os.getenv("APPROVAL_EMAIL")

#     # Validate configuration
#     required_values = {
#         "SMTP_HOST": smtp_host,
#         "SMTP_USER": smtp_user,
#         "SMTP_PASSWORD": smtp_password,
#         "APPROVAL_EMAIL": recipient,
#     }

#     missing = [
#         key for key, value in required_values.items()
#         if not value
#     ]

#     if missing:
#         raise ValueError(
#             f"Missing environment variables: {', '.join(missing)}"
#         )

#     # Create email message
#     message = EmailMessage()

#     message["From"] = smtp_user
#     message["To"] = recipient
#     message["Subject"] = subject

#     message.set_content(body)

#     # Connect to Gmail SMTP
#     with smtplib.SMTP(smtp_host, smtp_port) as server:

#         # Enable TLS encryption
#         server.starttls()

#         # Login to Gmail
#         server.login(smtp_user, smtp_password)

#         # Send email
#         server.send_message(message)

#     print("Email sent successfully!")