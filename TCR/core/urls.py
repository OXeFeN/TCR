# core/urls.py
from django.contrib import admin
from django.urls import path, include
from .views import home, about
from users.views import register
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('users/', include('users.urls')),  # Nebo dle potřeby s prefixem, např. 'users/'
    #path('accounts/logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    #path('accounts/', include('django.contrib.auth.urls')),
]
