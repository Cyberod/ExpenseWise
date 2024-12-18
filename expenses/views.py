from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'expenses/index.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('expenses')
    return render(request, 'authentication/login.html')

def add_expense(request):
    return render(request, 'expenses/add_expense.html')