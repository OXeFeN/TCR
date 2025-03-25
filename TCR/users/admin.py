# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Role, UserRole, AuditLog

class UserRoleInline(admin.TabularInline):
    model = UserRole
    extra = 1

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = [UserRoleInline]
    
    # Zobrazovaná pole v seznamu uživatelů
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'membership_paid')
    
    # Přidáme vlastní pole do fieldsets pro úpravu uživatele
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Osobní informace', {'fields': ('first_name', 'last_name', 'email', 'membership_paid')}),
        ('Oprávnění', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Důležitá data', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldset pro vytváření nového uživatele v administraci
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'membership_paid', 'password1', 'password2', 'is_active', 'is_staff'),
        }),
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(UserRole)
admin.site.register(AuditLog)
