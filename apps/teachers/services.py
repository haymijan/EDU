# File: apps/teachers/services.py
from django.contrib.auth import get_user_model
from django.db import transaction
from .models import TeacherProfile

User = get_user_model()

@transaction.atomic
def create_teacher_service(data):
    # ১. ইউজার অ্যাকাউন্ট তৈরি
    user = User.objects.create_user(
        username=data['username'], password=data['password'],
        first_name=data['first_name'], last_name=data['last_name'], role='teacher'
    )
    if data.get('profile_picture'):
        user.profile_picture = data['profile_picture']
        user.save()
        
    # ২. টিচার প্রোফাইল তৈরি (শিফট সহ)
    teacher = TeacherProfile.objects.create(
        user=user,
        employee_id=data['employee_id'],
        designation=data['designation'],
        qualification=data['qualification'],
        phone_number=data.get('phone_number', ''),
        address=data.get('address', ''),
        gender=data.get('gender', 'male'),
        blood_group=data.get('blood_group', ''),
        salary=data.get('salary', 0.00),
        shift=data.get('shift', 'morning')  # নতুন শিফট ফিল্ড যুক্ত করা হলো
    )
    
    # ৩. সাবজেক্ট সেভ করা (ManyToMany Field)
    if 'subject_ids' in data and data['subject_ids']:
        teacher.subjects.set(data['subject_ids'])
        
    return teacher

@transaction.atomic
def update_teacher_service(teacher_id, data):
    teacher = TeacherProfile.objects.select_related('user').get(id=teacher_id)
    user = teacher.user

    # ১. ইউজার প্রোফাইল আপডেট
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    if data.get('profile_picture'):
        user.profile_picture = data['profile_picture']
    user.save()

    # ২. টিচার প্রোফাইল আপডেট (শিফট সহ)
    teacher.employee_id = data.get('employee_id', teacher.employee_id)
    teacher.designation = data.get('designation', teacher.designation)
    teacher.qualification = data.get('qualification', teacher.qualification)
    teacher.phone_number = data.get('phone_number', teacher.phone_number)
    teacher.address = data.get('address', teacher.address)
    teacher.gender = data.get('gender', teacher.gender)
    teacher.blood_group = data.get('blood_group', teacher.blood_group)
    teacher.salary = data.get('salary', teacher.salary)
    teacher.shift = data.get('shift', teacher.shift)  # শিফট আপডেট লজিক
    teacher.save()
    
    # ৩. সাবজেক্ট লিস্ট আপডেট করা (ManyToMany Field)
    if 'subject_ids' in data:
        teacher.subjects.set(data['subject_ids'])
    
    return teacher