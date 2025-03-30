from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'start_hour', 'end_hour', 'created_at')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'date')
    ordering = ('-date', '-start_hour')

admin.site.register(Reservation, ReservationAdmin)