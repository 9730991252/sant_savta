from django.db import models

# Create your models here.
class Office_employee(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    post = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    
class Member(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    mobile = models.IntegerField()
    pin = models.IntegerField()
    status = models.IntegerField(default=1)
    
class Group_name(models.Model):
    name = models.CharField(max_length=100, default='')
    address = models.CharField(max_length=1000, default='')
    member_installment_limit = models.FloatField(default=0)
    maximum_loan = models.FloatField(default=0)
    loan_interest = models.FloatField(default=0)
    date = models.DateField(auto_now_add=True,null=True)
    
class Member_installment(models.Model):
    member = models.ForeignKey(Member,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    amount = models.FloatField()
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Member_loan(models.Model):
    member = models.ForeignKey(Member,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    loan_amount = models.FloatField()
    minimum_loan_installment = models.FloatField(default=0) 
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    loan_status = models.IntegerField(default=1)
    
class Member_loan_installment(models.Model):
    member = models.ForeignKey(Member,on_delete=models.PROTECT,null=True)
    loan = models.ForeignKey(Member_loan,on_delete=models.PROTECT,null=True)
    office_employee = models.ForeignKey(Office_employee,on_delete=models.PROTECT,null=True)
    installment_amount = models.FloatField()
    interest_amount = models.FloatField(null=True)
    date = models.DateField(auto_now_add=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
class Loan_demand(models.Model):
    member = models.ForeignKey(Member,on_delete=models.PROTECT,null=True)
    demand_amount = models.FloatField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    