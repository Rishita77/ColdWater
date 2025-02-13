from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_email(to_email, subject, plain_text, html_content):
    """
    Sends an email using SendGrid.
    
    Parameters:
        to_email (str or list): Recipient email(s). Can be a single email or a list of emails.
        subject (str): Subject of the email.
        plain_text (str): Plain text content of the email.
        html_content (str): HTML content of the email.
    
    Returns:
        int: The status code of the email send request.
    """
    try:
        sg = SendGridAPIClient('your_sendgrid_api_key')  # Replace with your SendGrid API key
        message = Mail(
            from_email='your_email@example.com',  # Replace with your verified sender email
            to_emails=to_email,
            subject=subject,
            plain_text_content=plain_text,
            html_content=html_content
        )
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return 500  # Return error status code
