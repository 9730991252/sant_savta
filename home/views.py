from django.shortcuts import redirect, render
from django.contrib import * 
from office.models import *
from datetime import date
# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('office_mobile'):
        return redirect('office_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            o = Office_employee.objects.filter(status=1, mobile=number, pin=pin).first()
            if o:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_home')
    return render(request, 'home/login.html')

def logout(request):
    if request.session.has_key('office_mobile'):
        del request.session['office_mobile']
    return redirect('/')