from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """
    Custom manager for User model to handle user and superuser creation.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """
    Custom User model that uses email instead of username for authentication.
    """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class EmailHistory(models.Model):
    """
    Model to store the history of emails sent using SendGrid.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="emails_sent")
    position = models.CharField(max_length=255)  # Position the email is about
    recipients = models.TextField()  # Store recipient emails as a comma-separated string
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the email was sent
    status = models.CharField(max_length=20, choices=[
        ("success", "Success"),
        ("failed", "Failed")
    ])
    error_details = models.TextField(blank=True, null=True)  # Store error details in case of failure

    def __str__(self):
        return f"Email for {self.position} - {self.status}"


class TemporaryFile(models.Model):
    """
    Model to store temporary files (CSV and PDF) if needed.
    These files will be cleaned up after processing.
    """
    file = models.FileField(upload_to="temp_files/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
