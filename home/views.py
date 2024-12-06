from django.shortcuts import redirect, render
from django.contrib import *
from office.models import *
from datetime import date
# Create your views here.
def index(request):
    # m.date = date(2024,11,29)
    return render(request, 'home/index.html')


def login(request):
    if request.session.has_key('office_mobile'):
        return redirect('office_home')
    if request.session.has_key('member_mobile'):
        return redirect('member_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            o = Office_employee.objects.filter(status=1, mobile=number, pin=pin).first()
            if o:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_home')
            m = Member.objects.filter(status=1, mobile=number, pin=pin).first()
            if m:
                request.session['member_mobile'] = request.POST["number"]
                return redirect('member_home')
    return render(request, 'home/login.html')

def logout(request):
    if request.session.has_key('office_mobile'):
        del request.session['office_mobile']
    if request.session.has_key('member_mobile'):
        del request.session['member_mobile']
    return redirect('/')