from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.decorators import login_required
from backend_app.utils.email_utils import send_email

def send_welcome_email(request):
    if request.method == "POST":
        # Example: Sending a welcome email to the registered user
        user_email = request.POST.get('email')  # Get user's email from POST request
        if user_email:
            status = send_email(
                to_email=user_email,
                subject="Welcome to Our Platform",
                plain_text="Thanks for joining us!",
                html_content="<strong>Welcome! We're glad to have you on board.</strong>"
            )
            if status == 202:  # HTTP status 202 indicates success
                return JsonResponse({"success": True, "message": "Email sent!"})
            else:
                return JsonResponse({"success": False, "message": "Failed to send email."})
    return JsonResponse({"success": False, "message": "Invalid request."})


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
