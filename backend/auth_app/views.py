from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth.decorators import login_required


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
