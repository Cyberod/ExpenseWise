from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from expenses.models import Expense
from userincome.models import UserIncome
import datetime

class DashboardViewTests(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")

        # Create some expenses and incomes
        self.expense1 = Expense.objects.create(
            owner=self.user,
            amount=100.0,
            category="Food",
            date=datetime.date.today() - datetime.timedelta(days=10),
            description="Grocery shopping",
        )
        self.expense2 = Expense.objects.create(
            owner=self.user,
            amount=200.0,
            category="Transport",
            date=datetime.date.today() - datetime.timedelta(days=20),
            description="Bus fare",
        )
        self.income1 = UserIncome.objects.create(
            owner=self.user,
            amount=500.0,
            source="Salary",
            date=datetime.date.today() - datetime.timedelta(days=15),
            description="Monthly salary",
        )
        self.income2 = UserIncome.objects.create(
            owner=self.user,
            amount=150.0,
            source="Freelance",
            date=datetime.date.today() - datetime.timedelta(days=5),
            description="Project payment",
        )

    def test_dashboard_authenticated_access(self):
        # Test that authenticated users can access the dashboard
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('expense_category_data', response.json())
        self.assertIn('income_source_data', response.json())

    def test_dashboard_unauthenticated_access(self):
        # Test that unauthenticated users are redirected
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn("authentication/login", response.url)

    def test_dashboard_with_empty_data(self):
        # Test dashboard response with no expenses or income
        Expense.objects.all().delete()
        UserIncome.objects.all().delete()

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['expense_category_data'], {})
        self.assertEqual(response.json()['income_source_data'], {})

    def test_dashboard_with_valid_data(self):
        # Test aggregation of expense and income data
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        expense_data = response.json()['expense_category_data']
        income_data = response.json()['income_source_data']

        self.assertEqual(expense_data["Food"], 100.0)
        self.assertEqual(expense_data["Transport"], 200.0)
        self.assertEqual(income_data["Salary"], 500.0)
        self.assertEqual(income_data["Freelance"], 150.0)

    def test_dashboard_date_range_filtering(self):
        # Test that only data within the last 6 months is included
        six_months_ago = datetime.date.today() - datetime.timedelta(days=30 * 6)

        # Add old data outside the date range
        Expense.objects.create(
            owner=self.user,
            amount=300.0,
            category="Old Expense",
            date=six_months_ago - datetime.timedelta(days=1),
            description="Too old",
        )
        UserIncome.objects.create(
            owner=self.user,
            amount=400.0,
            source="Old Income",
            date=six_months_ago - datetime.timedelta(days=1),
            description="Too old",
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        expense_data = response.json()['expense_category_data']
        income_data = response.json()['income_source_data']

        self.assertNotIn("Old Expense", expense_data)
        self.assertNotIn("Old Income", income_data)

    def test_dashboard_edge_case_date(self):
        # Test that data exactly 6 months ago is included
        six_months_ago = datetime.date.today() - datetime.timedelta(days=30 * 6)

        Expense.objects.create(
            owner=self.user,
            amount=50.0,
            category="Edge Case Expense",
            date=six_months_ago,
            description="Exact date edge case",
        )
        UserIncome.objects.create(
            owner=self.user,
            amount=75.0,
            source="Edge Case Income",
            date=six_months_ago,
            description="Exact date edge case",
        )

        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        expense_data = response.json()['expense_category_data']
        income_data = response.json()['income_source_data']

        self.assertIn("Edge Case Expense", expense_data)
        self.assertIn("Edge Case Income", income_data)
