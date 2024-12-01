from django.urls import path
from . import views
urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('collection/', views.collection, name='collection'),
    path('loan/', views.loan, name='loan'),
    path('members/', views.members, name='members'),
    path('profile/', views.profile, name='profile'),
]