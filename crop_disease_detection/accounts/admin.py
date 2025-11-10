from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustUser

class CustUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_farmer', 'is_admin', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    list_filter = ('is_farmer', 'is_admin', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_farmer', 'is_admin')}),
    )

admin.site.register(CustUser, CustUserAdmin)
