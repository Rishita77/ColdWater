from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_files_and_send_email, name='upload_files'),
    path('welcome-email/', views.send_welcome_email, name='welcome_email'),
]
