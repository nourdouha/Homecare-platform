from django.urls import  path
from django.http.response import HttpResponse
from user import views



urlpatterns = [
    path('users/', views.aPage),
]