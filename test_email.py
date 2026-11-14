from services.email_service import send_email


send_email(
    subject="DevOps AI Agent - SMTP Test",
    body="""
Hello!

This is a test email from my DevOps AI Agent.

Gmail SMTP integration is working successfully.

Regards,
DevOps AI Agent
"""
)