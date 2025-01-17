from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from ..models import UserPreference
import os
import json


class UserPreferenceViewTests(TestCase):
    def setUp(self):
        """
        Set up test client, user, and user preference data.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        self.preferences_url = reverse('preferences')
        self.currencies_file_path = os.path.join('currencies.json')

        # Simulate currencies.json file
        self.currencies_data = {"USD": "United States Dollar", "EUR": "Euro"}
        with open(self.currencies_file_path, 'w') as file:
            json.dump(self.currencies_data, file)

    def tearDown(self):
        """
        Clean up after tests.
        """
        if os.path.exists(self.currencies_file_path):
            os.remove(self.currencies_file_path)

    def test_index_view_get(self):
        """
        Test GET request to index view.
        """
        response = self.client.get(self.preferences_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'preferences/index.html')
        self.assertIn('currencies', response.context)
        self.assertEqual(len(response.context['currencies']), len(self.currencies_data))

    def test_index_view_post_create_preference(self):
        """
        Test POST request to create a new user preference.
        """
        response = self.client.post(self.preferences_url, {'currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(UserPreference.objects.filter(user=self.user, currency='USD').exists())
        self.assertContains(response, 'Currency successfully set to USD')

    def test_index_view_post_update_preference(self):
        """
        Test POST request to update an existing user preference.
        """
        UserPreference.objects.create(user=self.user, currency='EUR')
        response = self.client.post(self.preferences_url, {'currency': 'USD'})
        self.assertEqual(response.status_code, 200)
        user_pref = UserPreference.objects.get(user=self.user)
        self.assertEqual(user_pref.currency, 'USD')
        self.assertContains(response, 'Currency successfully changed to USD')

    # work on this
    def test_index_view_invalid_post(self):
        """
        Test POST request with invalid data.
        """
        response = self.client.post(self.preferences_url, {'currency': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Currency successfully set to')
        self.assertFalse(UserPreference.objects.filter(user=self.user).exists())
