from django.urls import path
from .views import register, dashboard, profile_view, user_management, delete_user, delete_users_bulk, edit_profile, admin_edit_user
from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView, PasswordChangeDoneView

urlpatterns = [
    path('accounts/login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('register/', register, name='registration'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile/', profile_view, name='profile'),
    path('manage-users/', user_management, name='user_management'),
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('delete-users/', delete_users_bulk, name='delete_users_bulk'),
    #path('logout/', LogoutView.as_view(template_name='users/logged_out.html'), name='logout'),
    path('profil/edit/', edit_profile, name='edit_profile'),
    path('profil/heslo/', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('profil/heslo-hotovo/', PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),
    path('admin/users/edit/<int:user_id>/', admin_edit_user, name='admin_edit_user'),
]