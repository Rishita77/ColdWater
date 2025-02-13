from rest_framework import serializers
from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        # Create a new user instance with the provided validated data
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user information.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'is_active', 'is_staff')
