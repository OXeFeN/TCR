from django.urls import path
from .views import register, dashboard, profile_view
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', register, name='registration'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    #path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),

]