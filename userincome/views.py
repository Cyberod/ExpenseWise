from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserIncome, Source
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
import json
from django.http import JsonResponse,HttpResponse
import datetime
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
import csv
import xlwt




def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)

@login_required(login_url='authentication/login')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = currency = UserPreference.objects.get_or_create(user=request.user)[0].currency



    context = {
        'sources': sources,
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    print(sources)
    return render(request, 'income/index.html', context)


@login_required(login_url='authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
        }
    if request.method == 'GET':
        return render(request, 'income/add_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date'] or now()
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render (request, 'income/add_income.html', context)
        
        UserIncome.objects.create(owner=request.user, amount=amount, description=description, date=date, source=source)
        messages.success(request, 'Income added successfully')
        return redirect('income')
    


def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources
    }

    if request.method == 'GET':
        return render(request, 'income/edit-income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/income-edit.html', context)
        
        if not description:
            messages.error(request, 'Description is required')
            return render (request, 'incomes/income-edit.html', context)
        
        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()
        messages.success(request, 'Income added successfully')
        return redirect('income')
    
@require_POST
def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully')
    return redirect('income')


def income_source_summary(request):

    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    income = UserIncome.objects.filter(owner=request.user, date__gte = six_months_ago, date__lte = todays_date)
    finalrep = {}

    def get_source(income):
        return income.source

    
    source_list = list(set(map(get_source, income))) #returns a distinct list of categories


    """ 
        returns a list of dictionaries, where each dictionary contains the Source and the amount received from that source
    """
    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)

        for item in filtered_by_source:
            amount += item.amount
        return amount

    for i in income:
        for j in source_list:
            finalrep[j] = get_income_source_amount(j)

    print('income data:',finalrep)

    return JsonResponse({'income_source_data': finalrep}, safe=False)

def income_stats_view(request):
    return render(request, 'Income/income_stats.html')



def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=Incomes' + str(datetime.datetime.now()) + '.csv'

    writer = csv.writer(response)
    writer.writerow(['Source', 'Amount', 'Description', 'Date'])
    
    incomes = UserIncome.objects.filter(owner=request.user)
    
    for income in incomes:
        writer.writerow([
            income.source,
            income.amount, 
            income.description, 
            income.date.strftime('%m-%d-%y')
            ])
    
    return response


def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Incomes' + str(datetime.datetime.now()) + '.xls'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Incomes')

    row_num = 0
    font_style = xlwt.XFStyle()

    font_style.font.bold = True

    columns = ['Source', 'Amount', 'Description', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = UserIncome.objects.filter(owner=request.user).values_list('source', 'amount', 'description', 'date')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename=Incomes' + str(datetime.datetime.now()) + '.pdf'

    response['Content-Transfer-Encoding'] = 'binary'

    incomes = UserIncome.objects.filter(owner=request.user)

    sum = incomes.aggregate(Sum('amount'))

    html_string = render_to_string('income/pdf-output.html', {'incomes': incomes, 'total': sum['amount__sum'] })

    html = HTML(string=html_string)
    result = html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()

        output = open(output.name, 'rb')
        response.write(output.read())

    return response




def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    income = UserIncome.objects.filter(owner=request.user, 
                                     date__gte=six_months_ago, 
                                     date__lte=todays_date)
    finalrep = {}

    def get_source(income):
        return income.source
    
    source_list = list(set(map(get_source, income)))

    def get_income_source_amount(source):
        amount = 0
        filtered_by_source = income.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    for source in source_list:
        finalrep[source] = get_income_source_amount(source)

    return JsonResponse({'income_source_data': finalrep}, safe=False)


