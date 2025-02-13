from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from backend_app.utils.email_utils import send_email
from django.views.decorators.csrf import csrf_exempt
from .serializers import RegisterSerializer, LoginSerializer
from django.core.files.storage import default_storage
import csv
from sendgrid.helpers.mail import Attachment, FileContent, FileName, FileType, Disposition


@csrf_exempt
def upload_files_and_send_email(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv")
        pdf_file = request.FILES.get("pdf")
        position = request.POST.get("position")

        if not csv_file or not pdf_file or not position:
            return JsonResponse({"error": "Missing required files or data."}, status=400)

        # Process CSV File to Extract Email Addresses
        email_list = []
        try:
            decoded_csv = csv_file.read().decode('utf-8').splitlines()
            csv_reader = csv.reader(decoded_csv)
            for row in csv_reader:
                if row:  # Ensure row is not empty
                    email_list.append(row[0])  # Assuming email addresses are in the first column
        except Exception as e:
            return JsonResponse({"error": "Invalid CSV format."}, status=400)

        if not email_list:
            return JsonResponse({"error": "No valid email addresses found in the CSV."}, status=400)

        # Read PDF File Content
        pdf_content = pdf_file.read()

        # Create and Send Email Using SendGrid
        try:
            message_body = f"""
                <p>Hi there!</p>
                <p>We are excited to share this opportunity for the position of <strong>{position}</strong>.</p>
                <p>Please find the attached document for more details.</p>
            """
            status = send_email(
                to_email=email_list,
                subject=f"Exciting Opportunity for {position}",
                plain_text="We are excited to share this opportunity with you.",
                html_content=message_body,
            )
            if status == 202:  # HTTP status 202 indicates success
                return JsonResponse({"message": "Email sent successfully to all recipients!"})
            else:
                return JsonResponse({"error": "Failed to send emails."}, status=500)

        except Exception as e:
            return JsonResponse({"error": "Failed to send emails.", "details": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Send a welcome email to the user
        user_email = serializer.validated_data.get('email')
        send_email(
            to_email=user_email,
            subject="Welcome to Our Platform",
            plain_text="Thank you for registering with us.",
            html_content="<strong>Welcome to our platform! We're excited to have you.</strong>",
        )
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
