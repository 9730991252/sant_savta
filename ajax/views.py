from django.http import *
from django.shortcuts import *
from django.template.loader import *
from django.db.models import Q
from office.models import *
def member_details(request):
    if request.method == 'GET':
        c = ''
        id = request.GET['id']
        m = Member.objects.filter(id=id).first()
        group_name = Group_name.objects.all().last()
        context={
            'm':m,
            'group_name':group_name,
        }
        t = render_to_string('ajax/office/member_details.html', context)
    return JsonResponse({'t': t})

def member_details_loan(request):
    if request.method == 'GET':
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        c = ''
        id = request.GET['id']
        m = Member.objects.filter(id=id).first()
        group_name = Group_name.objects.all().last()
        context={
            'm':m,
            'group_name':group_name,
            'office_empoyee':office_empoyee
        }
        t = render_to_string('ajax/office/member_details_loan.html', context)
    return JsonResponse({'t': t})