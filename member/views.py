from django.shortcuts import redirect, render
from office.models import *
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def member_home(request):
    if request.session.has_key('member_mobile'):
        m = request.session['member_mobile']
        member = Member.objects.filter(mobile=m).first()
        if member:
            total_member_installment = Member_installment.objects.filter(member_id=member.id).aggregate(Sum('amount'))
            

            
        else:
            del request.session['member_mobile']
            return redirect('login')
        context={
            'member':member,
            'members':Member.objects.all(),
            'member_installment':Member_installment.objects.filter(member_id=member.id).order_by('-id'),
            'total_member_installment':total_member_installment['amount__sum']
        }
        return render(request, 'member/member_home.html', context)
    else:
        return redirect('login')