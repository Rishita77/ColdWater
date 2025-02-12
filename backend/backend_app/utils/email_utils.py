from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to_email, subject, plain_text, html_content):
    """
    Sends an email using SendGrid API.
    """
    message = Mail(
        # Replace with your verified SendGrid email
        from_email="your-email@example.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=plain_text,
        html_content=html_content
    )

    try:
        # Fetch API key from settings
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent! Status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
