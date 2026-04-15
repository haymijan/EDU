# File: apps/students/admin.py
from django.contrib import admin
from .models import Student, AcademicSession, AdmissionCategory, BloodGroup

# ================= MASTER DATA ADMIN =================

@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(AdmissionCategory)
class AdmissionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(BloodGroup)
class BloodGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

# ================= STUDENT ADMIN =================

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # is_active বাদ দিয়ে আমাদের নতুন ডাইনামিক ফিল্ডগুলো (session, category) যুক্ত করা হয়েছে
    list_display = ('roll_number', 'get_full_name', 'classroom', 'section', 'session', 'guardian_phone')
    list_filter = ('classroom', 'section', 'session', 'gender', 'blood_group')
    search_fields = ('roll_number', 'user__first_name', 'user__last_name', 'guardian_phone')
    
    # অ্যাডমিন প্যানেলে একসাথে নাম দেখানোর জন্য
    def get_full_name(self, obj):
        if obj.user:
            return f"{obj.user.first_name} {obj.user.last_name}"
        return "Unknown"
    get_full_name.short_description = 'Student Name'