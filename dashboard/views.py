from django.shortcuts import render

from expenses.models import Expense
from userincome.models import UserIncome
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='authentication/login')
def dashboard(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    expenses = Expense.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte = todays_date)
    income = UserIncome.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte = todays_date)
    expense_finalrep = {}
    income_finalrep = {}

    def get_category(expense):
        return expense.category
    
    def get_source(income):
        return income.source
    
    

    
    category_list = list(set(map(get_category, expenses))) #returns a distinct list of categories
    source_list = list(set(map(get_source, income))) #returns a distinct list of sources


    """ 
        returns a list of dictionaries, where each dictionary contains the category and the amount spent in that category
    """
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)

        for item in filtered_by_category:
            amount += item.amount
        return amount
    
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for i in income:
        for j in source_list:
            income_finalrep[j] = get_income_source_amount(j)

    for x in expenses:
        for y in category_list:
            expense_finalrep[y] = get_expense_category_amount(y)


    return JsonResponse({
        'expense_category_data': expense_finalrep, 
        'income_source_data': income_finalrep }, safe=False)


def dashboard_stats(request):
    return render(request, 'dashboard/dashboard_stats.html')


