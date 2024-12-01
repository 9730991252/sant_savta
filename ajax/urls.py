from django.urls import path
from . import views
urlpatterns = [
    path('member_details/', views.member_details, name='member_details'),
    path('member_details_loan/', views.member_details_loan, name='member_details_loan'),

]