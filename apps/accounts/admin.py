# File: apps/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# কাস্টম ইউজার মডেলটি অ্যাডমিন প্যানেলে রেজিস্টার করা হলো
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # অ্যাডমিন প্যানেলের লিস্ট ভিউতে কোন কোন কলাম দেখাবে
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    
    # ইউজার এডিট করার সময় রোল (Role) ফিল্ডটি দেখানোর জন্য নিচের অংশটুকু যুক্ত করুন
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    
    # নতুন ইউজার তৈরির সময় রোল ফিল্ড যুক্ত করার জন্য
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'phone_number')}),
    )