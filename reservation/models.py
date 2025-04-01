from django.db import models
from django.conf import settings  # Importujeme nastavení

class Reservation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Použijeme dynamický odkaz na custom uživatele
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    date = models.DateField()
    start_hour = models.PositiveSmallIntegerField()
    end_hour = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_hour__gte=6) & models.Q(start_hour__lte=21),
                name='valid_start_hour'
            ),
            models.CheckConstraint(
                check=models.Q(end_hour__gte=7) & models.Q(end_hour__lte=22),
                name='valid_end_hour'
            ),
            models.CheckConstraint(
                check=models.Q(end_hour__gt=models.F('start_hour')),
                name='end_after_start'
            ),
        ]
        ordering = ['date', 'start_hour']

    def __str__(self):
        return f"{self.date} {self.start_hour}:00-{self.end_hour}:00 rezervace pro {self.user.username}"
    