from django.urls import path
from . import views
urlpatterns = [
    path('member_home/', views.member_home, name='member_home')
]