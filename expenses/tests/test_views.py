from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Expense, Category
import datetime
from django.utils.timezone import now

class ExpenseViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.category = Category.objects.create(name='Test Category')
        self.expense = Expense.objects.create(
            owner=self.user,
            amount=50.00,
            description='Test Expense',
            category=self.category.name,
            date=now()
        )
        self.client.login(username='testuser', password='password')

    def test_index_view(self):
        response = self.client.get(reverse('expenses'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/index.html')
        self.assertIn('categories', response.context)
        self.assertIn('page_obj', response.context)
        self.assertIn('currency', response.context)
        

    def test_add_expense_view_post_invalid_data(self):
        response = self.client.post(reverse('add-expense'), {
            'amount': '',  # Invalid amount
            'description': 'Invalid Test Expense',
            'expense_date': '2023-01-01',  # Required field
            'category': self.category.name  # Required field
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/add_expense.html')
        self.assertFalse(Expense.objects.filter(description='Invalid Test Expense').exists())



    def test_add_expense_view_post_valid_data(self):
        response = self.client.post(reverse('add-expense'), {
            'amount': 100.00,
            'description': 'Another Test Expense',
            'expense_date': '2023-01-01',
            'category': self.category.name
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expense.objects.filter(description='Another Test Expense').exists())

    def test_add_expense_view_post_invalid_data(self):
        response = self.client.post(reverse('add-expense'), {
            'amount': '',  # Missing amount
            'description': 'Invalid Test Expense'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/add_expense.html')
        self.assertFalse(Expense.objects.filter(description='Invalid Test Expense').exists())

    def test_expense_edit_view_get(self):
        response = self.client.get(reverse('expense-edit', args=[self.expense.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/edit-expense.html')

    def test_expense_edit_view_post_valid_data(self):
        response = self.client.post(reverse('expense-edit', args=[self.expense.id]), {
            'amount': 75.00,
            'description': 'Updated Test Expense',
            'expense_date': '2023-01-02',
            'category': self.category.name
        })
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 75.00)
        self.assertEqual(self.expense.description, 'Updated Test Expense')


    def test_expense_edit_view_post_invalid_data(self):
        response = self.client.post(reverse('expense-edit', args=[self.expense.id]), {
            'amount': '',  # Invalid amount
            'description': 'Invalid Update',
            'expense_date': '2023-01-01',  # Required field
            'category': self.category.name  # Required field
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'expenses/expense-edit.html')  # Updated template path
        self.expense.refresh_from_db()
        self.assertNotEqual(self.expense.description, 'Invalid Update')



    def test_expense_delete_view(self):
        response = self.client.post(reverse('expense-delete', args=[self.expense.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(id=self.expense.id).exists())

    def test_export_csv_view(self):
        response = self.client.get(reverse('export-csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_export_excel_view(self):
        response = self.client.get(reverse('export-excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/ms-excel')

    def test_export_pdf_view(self):
        response = self.client.get(reverse('export-pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
