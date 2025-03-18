from django.urls import path
from .views import register, dashboard

urlpatterns = [
    path('register/', register, name='registration'),
    path('dashboard/', dashboard, name='dashboard'),
]