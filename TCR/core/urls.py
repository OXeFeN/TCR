# core/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home, about
from users.views import register

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('users/', include('users.urls')),  # Nebo dle potřeby s prefixem, např. 'users/'
    path('accounts/', include('django.contrib.auth.urls')),
]
