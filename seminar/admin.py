from django.contrib import admin
from .models import User, Uloge, Predmeti, Upisi
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'uloga')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'uloga')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions')}),
    )


admin.site.register(User)
admin.site.register(Uloge)
admin.site.register(Predmeti)
admin.site.register(Upisi)


