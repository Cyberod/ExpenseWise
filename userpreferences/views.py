from django.shortcuts import render
import os
from django.conf import settings
import json
from .models import UserPreference
from django.contrib import messages

# Create your views here.



def index(request):

    exists = UserPreference.objects.filter(user=request.user).exists()

    currency_data = []
    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')

    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for key, value in data.items():
            currency_data.append({'name': key, 'value': value})

    context = {
        'currencies': currency_data,
    }
    user_preferences = None

    if exists:
        user_preferences = UserPreference.objects.get(user=request.user)

    if request.method == 'GET':
        return render(request, 'preferences/index.html', context)
    else:
        currency = request.POST['currency']
        context = {
            'currencies': currency_data,
            'user_preferences': user_preferences,
        }
        
        if exists:
            user_preferences.currency = currency
            user_preferences.save()
            messages.success(request, f'Currency successfully changed to {currency}')
            return render(request, 'preferences/index.html', context,)
        else:
            UserPreference.objects.create(user=request.user, currency=currency)
            messages.success(request, f'Currency successfully set to {currency}')
            return render(request, 'preferences/index.html', context)

