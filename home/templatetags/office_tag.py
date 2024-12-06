from django import template
from office.models import *
from django.db.models import Avg, Sum, Min, Max
from math import *
import math
from datetime import date
register = template.Library()
@register.simple_tag()
def available_amount():
    total_available_amount = 0
    total_installment= Member_installment.objects.all().aggregate(Sum('amount'))
    total_installment = total_installment['amount__sum']
    if total_installment:
        total_available_amount += total_installment
    if total_available_amount:
        m = Member_loan.objects.all().aggregate(Sum('loan_amount'))
        member_loan_amount = m['loan_amount__sum']
        if member_loan_amount:
            total_available_amount -= member_loan_amount
        ############
        loan_installment = Member_loan_installment.objects.all().aggregate(Sum('installment_amount'))
        loan_installment = loan_installment['installment_amount__sum']
        if loan_installment:
            total_available_amount += loan_installment
        ############
        loan_interest = Member_loan_installment.objects.all().aggregate(Sum('interest_amount'))
        loan_interest = loan_interest['interest_amount__sum']
        if loan_interest:
            loan_interest += loan_interest
        ############
        if total_available_amount:
            return total_available_amount
        else:
            return 0
    else:
        return 0
    
@register.simple_tag()
def check_collection_status(member_id):
    d = f'{date.today().year}-{date.today().month}'
    if Member_installment.objects.filter(date__icontains=d, member_id=member_id).exists():
        return 'yes' 
    else:
        return 'no'

@register.simple_tag()
def check_member_loan(member_id):
    member_loan = Member_loan.objects.filter(member_id=member_id, loan_status = 1).first()
    if member_loan:
        amount = member_loan.loan_amount
        g = Member_loan_installment.objects.filter(member_id=member_id).aggregate(Sum('installment_amount'))
        installment_amount = g['installment_amount__sum']
        if installment_amount:
            amount -= installment_amount
        return {'amount':amount, 'minimum_loan_installment': member_loan.minimum_loan_installment}
    else:
        return {'amount':0, 'minimum_loan_installment': 0}
    
@register.simple_tag()
def loan_interest_days(member_id):
    today_date = date.today()
    member_loan = Member_loan.objects.filter(member_id=member_id, loan_status = 1).first()
    if member_loan:
        member_loan_interest = Member_loan_installment.objects.filter(loan_id=member_loan.id).last()
        if member_loan_interest:
            day = (today_date - member_loan_interest.date)
        else:
            day = (today_date - member_loan.date)
        if day:
            if day is 0:
                return 30
            else:
                # return day.days
                return 30
        else:
            return 30
    else:
        return 30
    
@register.inclusion_tag('inclusion_tag/office/group_information.html')
def group_information():
    group = Group_name.objects.all().first()
    
    total_members = Member.objects.all().count()
    
    total_member_installment = Member_installment.objects.filter().aggregate(Sum('amount'))
    total_member_installment = total_member_installment['amount__sum']
    if total_member_installment is None:
        total_member_installment = 0 
        
    total_interest = Member_loan_installment.objects.filter().aggregate(Sum('interest_amount'))
    total_interest = total_interest['interest_amount__sum']
    if total_interest is None:
        total_interest = 0 
        
    total_pending_loan = Member_loan.objects.filter().aggregate(Sum('loan_amount'))
    total_pending_loan = total_pending_loan['loan_amount__sum']
    if total_pending_loan is None:
        total_pending_loan = 0 
    else:
        member_loan_installment = Member_loan_installment.objects.filter().aggregate(Sum('installment_amount'))
        member_loan_installment = member_loan_installment['installment_amount__sum']
        if member_loan_installment is None:
            member_loan_installment = 0
        else:
            total_pending_loan -= member_loan_installment
        
    return{
        'group':group,
        'total_members':total_members,
        'total_member_installment':total_member_installment,
        'total_interest':total_interest,
        'total_pending_loan':total_pending_loan,
        'member':Member.objects.all().order_by('-id')
    }
    
    
@register.inclusion_tag('inclusion_tag/office/member_detail.html')
def member_detail(member_id):
    group = Group_name.objects.all().first()
    
    member_installment_amount = Member_installment.objects.filter(member_id=member_id).aggregate(Sum('amount'))
    member_installment_amount = member_installment_amount['amount__sum']
    if member_installment_amount is None:
        member_installment_amount = 0 
        
    loan =  check_member_loan(member_id)
    loan = loan['amount']
    if loan == None:
        loan_interest = 0
    else:
        loan_interest = (int(loan) / 100) * group.loan_interest
        days = loan_interest_days(member_id)
        loan_interest = math.floor( (loan_interest * days) / 360) 
    return{
        'm':Member.objects.filter(id=member_id).first(),
        'member_installment_amount':member_installment_amount,
        'loan_interest':loan_interest
    }
    
@register.inclusion_tag('inclusion_tag/office/loan_installments_details.html')
def loan_installments_details(loan_id):
    loan_installment = Member_loan_installment.objects.filter(loan_id=loan_id)
    installment_amount_total = ''
    interest_amount_total = ''
    if loan_installment:
        installment_amount_total = loan_installment.aggregate(Sum('installment_amount'))
        installment_amount_total = installment_amount_total['installment_amount__sum']
        interest_amount_total = loan_installment.aggregate(Sum('interest_amount'))
        interest_amount_total = interest_amount_total['interest_amount__sum']
    
    return{
        'loan_installments':Member_loan_installment.objects.filter(loan_id=loan_id),
        'installment_amount_total':installment_amount_total,
        'interest_amount_total':interest_amount_total,
    }
    
@register.inclusion_tag('inclusion_tag/office/loan_demand_list.html')
def loan_demand_list():
    return{
        'loan_demand':Loan_demand.objects.all().order_by('date')
    }