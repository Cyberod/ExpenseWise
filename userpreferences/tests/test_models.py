from django.test import TestCase
from django.contrib.auth.models import User
from ..models import UserPreference


class UserPreferenceModelTests(TestCase):
    def setUp(self):
        """
        Set up test user and UserPreference instance.
        """
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.preference = UserPreference.objects.create(user=self.user, currency='USD')

    def test_user_preference_creation(self):
        """
        Test that a UserPreference instance is created correctly.
        """
        self.assertEqual(self.preference.user, self.user)
        self.assertEqual(self.preference.currency, 'USD')
        self.assertIsInstance(self.preference, UserPreference)

    # work on this
    def test_user_preference_str_representation(self):
        """
        Test the string representation of a UserPreference instance.
        """
        self.assertEqual(str(self.preference), "testuser'spreferences")

    def test_user_preference_update_currency(self):
        """
        Test updating the currency field of a UserPreference instance.
        """
        self.preference.currency = 'EUR'
        self.preference.save()
        updated_preference = UserPreference.objects.get(user=self.user)
        self.assertEqual(updated_preference.currency, 'EUR')

    def test_user_preference_one_to_one_relationship(self):
        """
        Test the one-to-one relationship between User and UserPreference.
        """
        duplicate_preference = UserPreference(user=self.user, currency='GBP')
        with self.assertRaises(Exception):
            duplicate_preference.save()

    def test_user_preference_with_blank_currency(self):
        """
        Test UserPreference instance with blank currency.
        """
        self.preference.currency = ''
        self.preference.save()
        self.assertEqual(self.preference.currency, '')
