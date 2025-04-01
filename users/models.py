from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    role_name = models.CharField(max_length=50, unique=True, verbose_name="Název role")
    description = models.TextField(blank=True, null=True, verbose_name="Popis role")

    def __str__(self):
        return self.role_name

class CustomUser(AbstractUser):
    # Pole děděná z AbstractUser: username, email, first_name, last_name, atd.
    membership_paid = models.BooleanField(default=False, verbose_name="Zaplacený členský příspěvek")
    # Vztah many-to-many k modelu Role, přes propojující tabulku UserRole
    roles = models.ManyToManyField(Role, through='UserRole', related_name="users", blank=True)

    def __str__(self):
        return self.username

class UserRole(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Uživatel")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, verbose_name="Role")

    class Meta:
        unique_together = (('user', 'role'),)
        verbose_name = "Přiřazení role"
        verbose_name_plural = "Přiřazení rolí"

    def __str__(self):
        return f"{self.user.username} - {self.role.role_name}"

# Volitelný: Model pro audit log, který eviduje akce uživatelů
class AuditLog(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Uživatel")
    action = models.CharField(max_length=255, verbose_name="Akce")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Čas akce")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP adresa")
    description = models.TextField(blank=True, null=True, verbose_name="Popis akce")

    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp})"
