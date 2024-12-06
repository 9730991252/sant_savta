from django.urls import path
from . import views
urlpatterns = [
    path('member_details/', views.member_details, name='member_details'),
    path('member_details_loan/', views.member_details_loan, name='member_details_loan'),
    path('check_backend_mobile', views.check_backend_mobile, name='check_backend_mobile')


]