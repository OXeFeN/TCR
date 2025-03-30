from django.urls import path
from . import views

urlpatterns = [
    # Kalendář rezervací
    path('', views.calendar_view, name='calendar'),
    path('create/', views.create_reservation, name='create_reservation'),
    # Administrace rezervací
    path('admin/', views.admin_reservations_view, name='admin_reservations'),
    path('admin/delete/<int:reservation_id>/', views.delete_reservation, name='delete_reservation'),
]