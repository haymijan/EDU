# File: apps/teachers/models.py

from django.db import models
from django.contrib.auth import get_user_model
from apps.students.models import BloodGroup

from apps.academics.models import Subject, AcademicShift


User = get_user_model()

# ================= HR MASTER DATA =================

class Designation(models.Model):
    name = models.CharField(max_length=100, unique=True) # যেমন: Principal, Senior Teacher

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True) # যেমন: Science, Admin

    def __str__(self):
        return self.name

class StaffType(models.Model):
    name = models.CharField(max_length=50, unique=True) # যেমন: Permanent, Guest Teacher

    def __str__(self):
        return self.name

class TeacherProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'), 
        ('female', 'Female')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    
    # --- ১. ডাইনামিক এইচআর (HR) লিংক ---
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    staff_type = models.ForeignKey(StaffType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # --- ২. ব্যক্তিগত ও সাধারণ তথ্য (আপনার আগের ফিল্ডগুলো) ---
    qualification = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    
    # --- ৩. ক্রস-মডিউল ডাইনামিক লিংক (Academics & Students থেকে) ---
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True, blank=True)
    shift = models.ForeignKey(AcademicShift, on_delete=models.SET_NULL, null=True, blank=True)
    subjects = models.ManyToManyField(Subject, blank=True)

    # --- ৪. ফিন্যান্স ও স্ট্যাটাস (আপনার আগের ফিল্ডগুলো) ---
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    joining_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"