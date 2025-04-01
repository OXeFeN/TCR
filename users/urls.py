from django.urls import path
from .views import register, dashboard, profile_view, user_management, delete_user, delete_users_bulk
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', register, name='registration'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('manage-users/', user_management, name='user_management'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete-users/', delete_users_bulk, name='delete_users_bulk'),
    #path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
]