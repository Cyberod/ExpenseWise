from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from authentication.tokens import app_activation_token

class AuthenticationViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password123')
        self.user.is_active = False
        self.user.save()
        self.login_url = reverse('login')


    def test_username_validation_valid(self):
        response = self.client.post(reverse('validate-username'), data={'username': 'validuser'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'username_valid': True})

    def test_username_validation_invalid(self):
        response = self.client.post(reverse('validate-username'), data={'username': 'invalid*user'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'username_error': 'username should only contain alphanumeric characters'})

    def test_username_already_exists(self):
        response = self.client.post(reverse('validate-username'), data={'username': 'testuser'}, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(response.content, {'username_error': 'username already exists'})

    def test_email_validation_valid(self):
        response = self.client.post(reverse('validate_email'), data={'email': 'newuser@example.com'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'email_valid': True})

    def test_email_validation_invalid(self):
        response = self.client.post(reverse('validate_email'), data={'email': 'invalid-email'}, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(response.content, {'email_error': 'email not valid'})

    def test_email_already_exists(self):
        response = self.client.post(reverse('validate_email'), data={'email': 'testuser@example.com'}, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(response.content, {'email_error': 'email already exists'})

    def test_register_user_success(self):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_existing_user(self):
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password123',
        }
        response = self.client.post(reverse('register'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Account already exists')

    def test_login_valid_credentials(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'password123'})
        self.assertRedirects(response, reverse('expenses'))


        #Recheck this
    def test_login_inactive_user(self):
        response = self.client.post(self.login_url, {
            'username': 'inactiveuser',
            'password': 'testpass'
        })
        self.user.is_active = False
        self.assertContains(
            response,
            'kindly go to your email to activate your account',
            html=True,
            msg_prefix="Couldn't find the expected message for inactive users"
        )  

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), data={'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

    def test_password_reset_valid_email(self):
        response = self.client.post(reverse('request-password'), data={'email': 'testuser@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Password reset link has been sent to your email')

    def test_password_reset_invalid_email(self):
        response = self.client.post(reverse('request-password'), data={'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No user found with this email')

    def test_account_activation_valid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = app_activation_token.make_token(self.user)
        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertRedirects(response, reverse('login'))

    def test_account_activation_invalid_token(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        response = self.client.get(reverse('activate', kwargs={'uidb64': uid, 'token': 'invalid-token'}))
        self.assertEqual(response.status_code, 302)  # Check for redirect status
        self.assertRedirects(response, reverse('register'))  # Verify redirect to register page
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)  # Verify user remains inactive

