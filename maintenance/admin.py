from django.contrib import admin
from .models import Machine, UserProfile

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number', 'location', 'status')
    list_filter = ('status',)
    search_fields = ('name', 'serial_number')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'phone_number')
    list_filter = ('role',)
    search_fields = ('user__username', 'department')
