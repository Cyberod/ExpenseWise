from django.test import TestCase
from django.contrib.auth.models import User
from ..models import UserIncome, Source
from django.utils.timezone import now


class UserIncomeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.source = Source.objects.create(name='Salary')
        self.income = UserIncome.objects.create(
            amount=1500.00,
            date=now(),
            description='Monthly salary',
            owner=self.user,
            source=self.source.name
        )

    def test_user_income_creation(self):
        """Test that a UserIncome instance is created successfully."""
        self.assertEqual(self.income.amount, 1500.00)
        self.assertEqual(self.income.description, 'Monthly salary')
        self.assertEqual(self.income.owner, self.user)
        self.assertEqual(self.income.source, 'Salary')

    # work on this
    def test_user_income_default_ordering(self):
        """Test that UserIncome objects are ordered by date in descending order."""
        another_income = UserIncome.objects.create(
            amount=1000.00,
            date=now(),
            description='Freelance work',
            owner=self.user,
            source=self.source.name
        )
        incomes = UserIncome.objects.all()
        self.assertEqual(incomes[0], another_income)
        self.assertEqual(incomes[1], self.income)

    def test_user_income_str_representation(self):
        """Test the string representation of UserIncome."""
        self.assertEqual(str(self.income), self.income.source)


class SourceModelTest(TestCase):
    def setUp(self):
        self.source = Source.objects.create(name='Freelance')

    def test_source_creation(self):
        """Test that a Source instance is created successfully."""
        self.assertEqual(self.source.name, 'Freelance')

    def test_source_str_representation(self):
        """Test the string representation of Source."""
        self.assertEqual(str(self.source), 'Freelance')

    # work on this
    def test_source_verbose_name_plural(self):
        """Test the verbose name plural of Source."""
        self.assertEqual(Source._meta.verbose_name_plural, 'Sources')
