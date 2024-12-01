from django.contrib import messages
from django.shortcuts import redirect, render
from office.models import *
# Create your views here.
def sunil_login(request):
    if request.method == 'POST':
        a =int(request.POST["number"])
        b =int(request.POST["pin"])
        s = a+b
        if s == 11000 :
            request.session['sunil_mobile'] = s
            return redirect('sunil_home')
        else:
            return redirect('sunil_login')
    return render(request, 'home/login.html')



def sunil_home(request):
    if request.session.has_key('sunil_mobile'):
        if 'add_office_employee'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            post = request.POST.get('post')
            # print('name' ,name, 'mobile' ,mobile, 'pin' ,pin, 'post' ,post)
            Office_employee(
                name = name,
                mobile = mobile,
                pin = pin,
                post = post,
            ).save()
        context={
            'office_empoyee':Office_employee.objects.all()
        }
        return render(request, 'sunil/sunil_home.html', context)
    else:
        return redirect('sunil')

