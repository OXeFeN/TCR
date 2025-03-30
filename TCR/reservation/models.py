from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, F

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    date = models.DateField()
    start_hour = models.PositiveSmallIntegerField()
    end_hour = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(start_hour__gte=0) & Q(start_hour__lte=23),
                name='valid_start_hour'
            ),
            models.CheckConstraint(
                check=Q(end_hour__gte=1) & Q(end_hour__lte=24),
                name='valid_end_hour'
            ),
            models.CheckConstraint(
                check=Q(end_hour__gt=F('start_hour')),
                name='end_after_start'
            ),
        ]
        ordering = ['date', 'start_hour']

    def __str__(self):
        return f"{self.date} {self.start_hour}:00-{self.end_hour}:00 rezervace pro {self.user.username}"