from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to_email, subject, plain_text, html_content):
    """
    Sends an email using SendGrid API.
    """
    message = Mail(
        from_email="your-email@example.com",  # Replace with your verified SendGrid email
        to_emails=to_email,
        subject=subject,
        plain_text_content=plain_text,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        if response.status_code == 202:  # Email sent successfully
            print(f"Email sent successfully! Status code: {response.status_code}")
            return response.status_code
        else:
            print(f"Failed to send email. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error sending email: {e}")
        return None
