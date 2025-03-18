from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('articles/', views.article_create, name='article_create'),
]
