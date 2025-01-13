from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from .tokens import app_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.contrib.auth.tokens import PasswordResetTokenGenerator




class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'username already exists'}, status=409)
        return JsonResponse({'username_valid': True}, status=200)


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'email not valid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'email already exists'}, status=409)
        return JsonResponse({'email_valid': True}, status=200)



    

class RegistrationView(View):

    def activate(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and app_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your account has been activated successfully. You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Activation link is invalid or has expired!')

        return redirect('register')


    def activate_email(self, request, user, to_email):
        email_subject = 'Activate your account' 
        message = render_to_string('authentication/activate_account.html', {
            'user': user,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': app_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        })
        email = EmailMessage(email_subject, message, to=[to_email])
        if email.send():
            messages.success(request, f'Dear <b>{user.username}</b>, kindly go to <b>{to_email}</b> inbox and click on the the recieved activation\
                link to activate your account and complete registration. <b>note:</b> also Check your spam folder')
        else:
            messages.error(request, f'Problem sending email to {to_email}, check if your email is typed correctly.')

    def get(self, request, *args, **kwargs):
        if kwargs.get('uidb64'):
            return self.activate(request, kwargs['uidb64'], kwargs['token'])
        else:
            return render(request, 'authentication/register.html')
        
    
    def post(self, request):
        # GET USER DATA
        # VALIDATE
        # CREATE A USER ACCOUNT
        # SAVE USER

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            "fieldValues": request.POST    
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)  
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_active = False
            user.save()
            self.activate_email(request, user, email)
            return render(request, 'authentication/register.html')


        messages.error(request, 'Account already exists')
        return render(request, 'authentication/register.html')

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f'Hello {user.username} you are logged in')
                    return redirect('expenses')
                messages.error(request, 'kindly go to your email to activate your account')
                return render(request, 'authentication/login.html')   
            messages.error(request, 'Invalid credentials')
            return render(request, 'authentication/login.html')
        messages.error(request, 'kindly fill all fields')
        return render(request, 'authentication/login.html')   


class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')          


class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset-password.html')

    def post(self, request):
        email = request.POST.get('email', '')
        context = {'values': request.POST}

        if not validate_email(email):
            messages.error(request, 'Please provide a valid email')
            return render(request, 'authentication/reset-password.html', context)

        user = User.objects.filter(email=email).first()
        if user:
            email_subject = 'Reset Your Password'
            message = render_to_string('authentication/reset-password-email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': PasswordResetTokenGenerator().make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'
            })
            
            email = EmailMessage(email_subject, message, to=[email])
            email.send()
            
            messages.success(request, 'Password reset link has been sent to your email')
        else:
            messages.error(request, 'No user found with this email')
            
        return render(request, 'authentication/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'authentication/set-new-password.html', context)

    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.error(request, 'Password reset link is invalid or has expired')
                return redirect('login')
            
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            
            if password1 != password2:
                messages.error(request, 'Passwords do not match')
                return render(request, 'authentication/set-new-password.html')
            
            if len(password1) < 6:
                messages.error(request, 'Password too short')
                return render(request, 'authentication/set-new-password.html')
            
            user.set_password(password1)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid password reset link')
            return redirect('login')
