# core/urls.py
from django.urls import path
from .views import home, about
from users.views import register

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
]
