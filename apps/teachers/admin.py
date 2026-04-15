# File: apps/teachers/admin.py
from django.contrib import admin
from .models import TeacherProfile

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'designation', 'phone_number', 'is_active')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('is_active', 'designation')

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    get_full_name.short_description = 'Teacher Name'