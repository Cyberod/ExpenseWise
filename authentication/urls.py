from .views import RegistrationView, UsernameValidationView, EmailValidationView, LoginView, LogoutView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('validate-username', csrf_exempt(UsernameValidationView.as_view()), name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate_email'),
    path('register', RegistrationView.as_view(), name="register"),
    path('activate/<uidb64>/<token>/', RegistrationView.as_view(), name='activate'),
    path('login', LoginView.as_view(), name="login"),
    path('Logout', csrf_exempt(LogoutView.as_view()), name="logout"),
]