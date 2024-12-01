from django.shortcuts import *
from .models import *
from django.contrib import messages
import time
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        if office_empoyee:
            pass
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'office_empoyee':office_empoyee,

        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def loan(request):
    if request.session.has_key('office_mobile'):
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        if office_empoyee:
            if 'add_loan_member'in request.POST:
                member_id = request.POST.get('member_id')
                loan_amount = request.POST.get('loan_amount')
                if Member_loan.objects.filter(member_id=member_id,loan_status=1).exists():
                    pass
                else:
                    Member_loan(
                        member_id = member_id,
                        office_employee_id=office_empoyee.id,
                        loan_amount = loan_amount,
                    ).save()
                time.sleep(1)        
                return redirect('loan')
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'office_empoyee':office_empoyee,
            'members':Member.objects.filter(status=1)
        }
        return render(request, 'office/loan.html', context)
    else:
        return redirect('login')
    
@csrf_exempt
def collection(request):
    if request.session.has_key('office_mobile'):
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        if office_empoyee:
            d = f'{date.today().year}-{date.today().month}'
            if 'add_amount'in request.POST:
                member_id = request.POST.get('member_id')
                amount = request.POST.get('amount')
                loan_installment = request.POST.get('loan_installment')
                loan_interest = request.POST.get('loan_interest')
                loan_amount = request.POST.get('loan_amount')
                if Member_installment.objects.filter(date__icontains=d, member_id=member_id).exists():
                    messages.warning(request,f"Member already Added")   
                else:
                    if int(loan_interest) is 0:
                        Member_installment(
                            member_id=member_id,
                            office_employee_id=office_empoyee.id,
                            amount=amount,
                        ).save()
                    if int(loan_interest) is not 0:
                        l = Member_loan.objects.filter(member_id=member_id, loan_status=1).last()
                        Member_installment(
                            member_id=member_id,
                            office_employee_id=office_empoyee.id,
                            amount=loan_installment,
                        ).save()
                        Member_loan_installment(
                            loan_id=l.id,
                            member_id=member_id,
                            office_employee_id=office_empoyee.id,
                            installment_amount=loan_amount,
                        ).save()
                        Member_loan_interest(
                            loan_id=l.id,
                            member_id=member_id,
                            office_employee_id=office_empoyee.id,
                            interest_amount=loan_interest,
                        ).save()
                        g = Member_loan_installment.objects.filter(member_id=member_id, loan_id=l.id).aggregate(Sum('installment_amount'))
                        installment_amount = g['installment_amount__sum']
                        total_pending_amount = (int(l.loan_amount) - int(installment_amount) )
                        if total_pending_amount == 0:
                            l.loan_status = 0
                            l.save()
                time.sleep(1)
                return redirect('collection')
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'office_empoyee':office_empoyee,
            'members':Member.objects.filter(status=1)
        }
        return render(request, 'office/collection.html', context)
    else:
        return redirect('login')
    
def profile(request):
    if request.session.has_key('office_mobile'):
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        if office_empoyee:
            if request.method == "POST":
                id = request.POST.get('id')
                name = request.POST.get('name')
                address = request.POST.get('address')
                member_installment_limit = request.POST.get('member_installment_limit')
                maximum_loan = request.POST.get('maximum_loan')
                loan_interest = request.POST.get('loan_interest')
                if id:
                    group = Group_name.objects.filter(id=id).first()
                    group.name = name
                    group.address = address
                    group.member_installment_limit = member_installment_limit
                    group.maximum_loan = maximum_loan
                    group.loan_interest = loan_interest
                    group.save()
                else:
                    Group_name(
                        name = name,
                        address = address,
                        member_installment_limit = member_installment_limit,
                        maximum_loan = maximum_loan,
                        loan_interest=loan_interest,
                    ).save()
                    
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'office_empoyee':office_empoyee,
            'group':Group_name.objects.all().last()
        }
        return render(request, 'office/profile.html', context)
    else:
        return redirect('login')
    
def members(request):
    if request.session.has_key('office_mobile'):
        m = request.session['office_mobile']
        office_empoyee = Office_employee.objects.filter(mobile=m).first()
        if office_empoyee:
            if 'add_member'in request.POST:
                name = request.POST.get('name')
                address = request.POST.get('address')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                if Member.objects.filter(mobile=mobile).exists():
                    messages.warning(request,f"Member already Exists - {mobile}")   
                else:
                    Member(
                        name = name,
                        address = address,
                        mobile = mobile,
                        pin = pin,
                    ).save()
                    messages.success(request,f"Member Added successfully - {name} - {mobile}")   
                time.sleep(1)
                return redirect('members')
            if 'edit_member'in request.POST:
                id = request.POST.get('id')
                name = request.POST.get('name')
                address = request.POST.get('address')
                mobile = request.POST.get('mobile')
                pin = request.POST.get('pin')
                Member(
                    id = id,
                    name = name,
                    address = address,
                    mobile = mobile,
                    pin = pin,
                ).save()
                messages.success(request,f"Member Edited successfully - {name} - {mobile}")   
                return redirect('members')
            if 'active'in request.POST:
                id = request.POST.get('id')
                c = Member.objects.filter(id=id).first()
                c.status = 0
                c.save()
                return redirect('members')
            if 'deactive'in request.POST:
                id = request.POST.get('id')
                c = Member.objects.filter(id=id).first()
                c.status = 1
                c.save()
                return redirect('members')
        else:
            del request.session['office_mobile']
            return redirect('login')
        context={
            'office_empoyee':office_empoyee,
            'members':Member.objects.all().order_by('name')
        }
        return render(request, 'office/members.html', context)
    else:
        return redirect('login')
   
                                                                                
                              
               
                                                                                
                    
                                                                                
                                              
                         
                                                   
                                                                                
 