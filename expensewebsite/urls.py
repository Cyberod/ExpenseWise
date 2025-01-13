
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('', include('expenses.urls')),
    path('authentication/', include('authentication.urls')),
    path('preferences/', include('userpreferences.urls')),
    path('Income/', include('userincome.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('admin/', admin.site.urls),
    
]
