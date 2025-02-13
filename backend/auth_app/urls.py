from django.urls import path
from .views import (
    register_user,
    login_user,
    logout_user,
    dashboard,
    send_welcome_email,
    upload_files_and_send_email,
)

urlpatterns = [
    path("register/", register_user, name="register_user"),
    path("login/", login_user, name="login_user"),
    path("logout/", logout_user, name="logout_user"),
    path("dashboard/", dashboard, name="dashboard"),
    path("send-welcome-email/", send_welcome_email, name="send_welcome_email"),
    path("upload-files-and-send-email/", upload_files_and_send_email, name="upload_files_and_send_email"),
]
