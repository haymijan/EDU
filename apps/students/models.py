# File: apps/students/models.py

from django.db import models
from django.contrib.auth import get_user_model
from apps.academics.models import ClassRoom, Section

User = get_user_model()

# ================= MASTER DATA MODELS (For Setup Dashboard) =================

class AcademicSession(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="যেমন: 2024, 2024-2025")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class AdmissionCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="যেমন: সাধারণ, হিফজ, এতিম")

    def __str__(self):
        return self.name

class BloodGroup(models.Model):
    name = models.CharField(max_length=10, unique=True, help_text="যেমন: A+, O-")

    def __str__(self):
        return self.name

# ================= MAIN STUDENT MODEL =================

class Student(models.Model):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )

    # ১. কোর ইউজার লিংক ও রোল
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    roll_number = models.CharField(max_length=20, unique=True)

    # ২. ডাইনামিক একাডেমিক লিংক (Master Data)
    session = models.ForeignKey(AcademicSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    category = models.ForeignKey(AdmissionCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    # ৩. ব্যক্তিগত তথ্য (ডাইনামিক ব্লাড গ্রুপসহ)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    # ৪. অভিভাবকের ও যোগাযোগের তথ্য
    guardian_name = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=15, null=True, blank=True)
    guardian_email = models.EmailField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True, help_text="জরুরি মোবাইল নম্বর")
    guardian_address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.roll_number})"