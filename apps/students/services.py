# File: apps/students/services.py

from django.contrib.auth import get_user_model
from django.db import transaction
from .models import Student
from apps.academics.models import ClassRoom, Section

User = get_user_model()

@transaction.atomic
def create_student_service(data):
    # ১. কাস্টম ইউজার তৈরি
    user = User.objects.create_user(
        username=data['username'],
        password=data['password'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role='student' 
    )
    
    # ছবি থাকলে সেটি ইউজারের প্রোফাইলে সেভ করা
    if data.get('profile_picture'):
        user.profile_picture = data['profile_picture']
        user.save()
        
    # ২. ক্লাস এবং সেকশনের অবজেক্ট খুঁজে বের করা
    classroom = None
    section = None
    if data.get('classroom_id'):
        classroom = ClassRoom.objects.filter(id=data['classroom_id']).first()
    if data.get('section_id'):
        section = Section.objects.filter(id=data['section_id']).first()
    
    # ৩. স্টুডেন্ট প্রোফাইল তৈরি
    student = Student.objects.create(
        user=user,
        roll_number=data['roll_number'],
        gender=data.get('gender', 'male'),
        classroom=classroom,
        section=section,
        guardian_phone=data.get('guardian_phone', ''),
        guardian_address=data.get('guardian_address', '') # ঠিকানা যুক্ত হলো
    )
    
    return student

@transaction.atomic
def update_student_service(student_id, data):
    student = Student.objects.select_related('user').get(id=student_id)
    user = student.user

    # ১. ইউজার তথ্য আপডেট
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    if data.get('profile_picture'):
        user.profile_picture = data['profile_picture']
    user.save()

    # ২. স্টুডেন্ট প্রোফাইল আপডেট
    student.roll_number = data.get('roll_number', student.roll_number)
    student.gender = data.get('gender', student.gender)
    student.guardian_phone = data.get('guardian_phone', student.guardian_phone)
    student.guardian_address = data.get('guardian_address', student.guardian_address)
    
    if data.get('classroom_id'):
        student.classroom = ClassRoom.objects.get(id=data['classroom_id'])
    if data.get('section_id'):
        student.section = Section.objects.get(id=data['section_id'])
    
    student.save()
    return student