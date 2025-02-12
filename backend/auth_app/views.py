from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.decorators import login_required
from backend_app.utils.email_utils import send_email
from django.conf import settings

import csv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage


def send_welcome_email(request):
    if request.method == "POST":
        user_email = request.POST.get('email')  # Get user's email from POST request
        if user_email:
            try:
                status = send_email(
                    to_email=user_email,
                    subject="Welcome to Our Platform",
                    plain_text="Thanks for joining us!",
                    html_content="<strong>Welcome! We're glad to have you on board.</strong>"
                )
                if status == 202:  # HTTP status 202 indicates success
                    return JsonResponse({"success": True, "message": "Email sent!"}, status=202)
                else:
                    return JsonResponse({"success": False, "message": "Failed to send email."}, status=500)
            except Exception as e:
                return JsonResponse({"success": False, "error": f"Error sending email: {str(e)}"}, status=500)
        else:
            return JsonResponse({"success": False, "message": "Email address not provided."}, status=400)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({'message': 'User registered successfully!'}, status=201)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful!'}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return JsonResponse(serializer.errors, status=400)


@api_view(['POST'])
def logout_user(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful!'}, status=200)


@login_required
def dashboard(request):
    return JsonResponse({'message': 'Welcome to your dashboard!'}, status=200)


@csrf_exempt
def upload_files_and_send_email(request):
    if request.method == "POST":
        try:
            csv_file = request.FILES.get("csv")
            pdf_file = request.FILES.get("pdf")
            position = request.POST.get("position")

            if not csv_file or not pdf_file or not position:
                return JsonResponse({"error": "Missing required files or data."}, status=400)

            # Validate file extensions
            if not csv_file.name.endswith('.csv') or not pdf_file.name.endswith('.pdf'):
                return JsonResponse({"error": "Invalid file format. Only CSV and PDF are allowed."}, status=400)

            # Process CSV File
            email_list = []
            try:
                decoded_csv = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(decoded_csv)
                for row in csv_reader:
                    if row:
                        email_list.append(row[0])  # Assuming email addresses are in the first column
            except Exception:
                return JsonResponse({"error": "Invalid CSV format or content."}, status=400)

            if not email_list:
                return JsonResponse({"error": "No valid email addresses found in the CSV."}, status=400)

            # Read PDF Content
            pdf_content = pdf_file.read()

            # Send Email Using SendGrid
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                message = Mail(
                    from_email="your-email@example.com",  # Replace with your email
                    to_emails=email_list,
                    subject=f"Exciting Opportunity for {position}",
                    html_content=f"""
                    <p>Hi there!</p>
                    <p>We are excited to share this opportunity for the position of <strong>{position}</strong>.</p>
                    <p>Please find the attached document for more details.</p>
                    """
                )

                # Attach PDF
                attachment = Attachment(
                    FileContent(pdf_content),
                    FileName(pdf_file.name),
                    FileType("application/pdf"),
                    Disposition("attachment"),
                )
                message.attachment = attachment

                # Send email
                sg.send(message)
                return JsonResponse({"message": "Email sent successfully to all recipients!"}, status=200)
            except Exception as e:
                return JsonResponse({"error": "Failed to send emails.", "details": str(e)}, status=500)

        except Exception as e:
            return JsonResponse({"error": "Unexpected error occurred.", "details": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
