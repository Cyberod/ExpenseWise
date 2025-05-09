from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', views.index, name='income'),
    path('add-income', views.add_income, name='add-income'),
    path('edit-income/<int:id>', views.income_edit, name='income-edit'),
    path('income-delete/<int:id>', views.income_delete, name='income-delete'),
    path('search-income', csrf_exempt(views.search_income), name='search_income'),
    path('income_source_summary', views.income_source_summary, name='income_summary'),
    path('income_stats', views.income_stats_view, name='income_stats'),
    path('export-csv', views.export_csv, name='export-csv'),
    path('export-excel', views.export_excel, name='export-excel'),
    path('export-pdf', views.export_pdf, name='export-pdf'),
    
]