from django.test import TestCase
from django.contrib.auth.models import User
from expenses.models import Expense, Category
from django.utils.timezone import now
import datetime

class ExpenseModelTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create test categories
        self.category1 = Category.objects.create(name="Food")
        self.category2 = Category.objects.create(name="Transport")

        # Create test expenses
        self.expense1 = Expense.objects.create(
            amount=50.0,
            description="Lunch at a restaurant",
            owner=self.user,
            category=self.category1.name,
            date=now()
        )
        self.expense2 = Expense.objects.create(
            amount=20.0,
            description="Bus fare",
            owner=self.user,
            category=self.category2.name,
            date=now() - datetime.timedelta(days=1)
        )

    def test_expense_creation(self):
        self.assertEqual(Expense.objects.count(), 2)
        self.assertEqual(self.expense1.owner, self.user)
        self.assertEqual(self.expense1.category, "Food")
        self.assertEqual(float(self.expense1.amount), 50.0)

    def test_expense_string_representation(self):
        self.assertEqual(str(self.expense1), "Food")
        self.assertEqual(str(self.expense2), "Transport")

    def test_expense_ordering(self):
        expenses = Expense.objects.all()
        self.assertEqual(expenses[0], self.expense1)  # Newest expense should come first

    def test_expense_category_field(self):
        self.assertEqual(self.expense1.category, "Food")
        self.assertEqual(self.expense2.category, "Transport")

    def test_expense_date_default(self):
        expense = Expense.objects.create(
            amount=15.0,
            description="Test default date",
            owner=self.user,
            category="Miscellaneous"
        )
        self.assertEqual(expense.date, now().date())

    def test_expense_owner_relationship(self):
        self.assertEqual(self.expense1.owner.username, "testuser")
        self.assertEqual(self.expense2.owner.username, "testuser")


class CategoryModelTestCase(TestCase):

    def setUp(self):
        # Create test categories
        self.category1 = Category.objects.create(name="Entertainment")
        self.category2 = Category.objects.create(name="Groceries")

    def test_category_creation(self):
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(self.category1.name, "Entertainment")
        self.assertEqual(self.category2.name, "Groceries")

    def test_category_string_representation(self):
        self.assertEqual(str(self.category1), "Entertainment")
        self.assertEqual(str(self.category2), "Groceries")

    def test_category_verbose_name_plural(self):
        self.assertEqual(Category._meta.verbose_name_plural, "Categories")
