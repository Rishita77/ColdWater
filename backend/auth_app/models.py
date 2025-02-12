from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


# User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No extra fields required during registration

    def __str__(self):
        return self.email


# Job Preferences Model
class JobPreference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_preferences')  # Links to User
    position = models.CharField(max_length=100)  # Selected position of interest

    def __str__(self):
        return f"{self.user.name} - {self.position}"


# Uploaded Files Model
class UploadedFiles(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')  # Links to User
    csv_file = models.FileField(upload_to='uploads/csv/', null=True, blank=True)  # For email CSV uploads
    resume_file = models.FileField(upload_to='uploads/resumes/', null=True, blank=True)  # For resume uploads
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp for uploads

    def __str__(self):
        return f"Files for {self.user.name}"

