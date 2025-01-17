from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import UserIncome, Source
import json
import datetime

class IncomeViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create sample sources and incomes
        self.source = Source.objects.create(name='Salary')
        self.income = UserIncome.objects.create(
            amount=5000,
            date=datetime.date.today(),
            description='Test Income',
            owner=self.user,
            source=self.source.name
        )

    def test_index_view(self):
        response = self.client.get(reverse('income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/index.html')
        self.assertIn('income', response.context)

    def test_add_income_get(self):
        response = self.client.get(reverse('add-income'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/add_income.html')

    def test_add_income_post_valid(self):
        data = {
            'amount': 3000,
            'description': 'Freelance work',
            'income_date': datetime.date.today(),
            'source': self.source.name
        }
        response = self.client.post(reverse('add-income'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('income'))
        self.assertTrue(UserIncome.objects.filter(description='Freelance work').exists())

    # work on this test
    def test_add_income_post_invalid(self):
        data = {
            'description': 'Invalid income',  # Missing amount
            'income_date': datetime.date.today(),
            'source': self.source.name
        }
        response = self.client.post(reverse('add-income'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/add_income.html')
        self.assertFalse(UserIncome.objects.filter(description='Invalid income').exists())

    def test_income_edit_get(self):
        response = self.client.get(reverse('income-edit', args=[self.income.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'income/edit-income.html')
        self.assertEqual(response.context['income'], self.income)

    def test_income_edit_post_valid(self):
        data = {
            'amount': 6000,
            'description': 'Updated Income',
            'income_date': datetime.date.today(),
            'source': self.source.name
        }
        response = self.client.post(reverse('income-edit', args=[self.income.id]), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('income'))
        updated_income = UserIncome.objects.get(id=self.income.id)
        self.assertEqual(updated_income.description, 'Updated Income')

    def test_income_delete(self):
        response = self.client.post(reverse('income-delete', args=[self.income.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('income'))
        self.assertFalse(UserIncome.objects.filter(id=self.income.id).exists())

    def test_search_income(self):
        data = {'searchText': 'Test Income'}
        response = self.client.post(reverse('search_income'), json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Test Income', str(response.content))

    def test_income_source_summary(self):
        response = self.client.get(reverse('income_summary'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.source.name, str(response.content))

    def test_export_csv(self):
        response = self.client.get(reverse('export-csv'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')

    def test_export_excel(self):
        response = self.client.get(reverse('export-excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/ms-excel')

    def test_export_pdf(self):
        response = self.client.get(reverse('export-pdf'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
