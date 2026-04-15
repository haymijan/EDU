# File: apps/accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

# ছবিগুলো রোল অনুযায়ী আলাদা ফোল্ডারে সেভ করার জন্য এই ফাংশনটি তৈরি করা হলো
def user_directory_path(instance, filename):
    # ইউজারের রোল অনুযায়ী ফোল্ডার তৈরি হবে (যেমন: STUDENT -> profiles/students/image.jpg)
    if instance.role:
        role_folder = f"{instance.role.lower()}s"
    else:
        role_folder = "others"
        
    return f'profiles/{role_folder}/{filename}'


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        TEACHER = 'TEACHER', 'Teacher'
        STUDENT = 'STUDENT', 'Student'
        PARENT = 'PARENT', 'Parent'

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.STUDENT)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    # upload_to এর জায়গায় ডাইনামিক ফাংশনটি যুক্ত করা হয়েছে
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"