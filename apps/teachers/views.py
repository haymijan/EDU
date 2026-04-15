# File: apps/teachers/views.py

from django.shortcuts import render, get_object_or_404
from .services import create_teacher_service, update_teacher_service
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from .models import TeacherProfile, Designation, Department, StaffType
from apps.students.models import BloodGroup
from apps.academics.models import Subject, AcademicShift
from django.db.models import Q


User = get_user_model()

#=========================================================================

def hr_setup_dashboard(request):
    designations = Designation.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    staff_types = StaffType.objects.all().order_by('name')
    
    return render(request, 'teachers/setup_dashboard.html', {
        'designations': designations,
        'departments': departments,
        'staff_types': staff_types
    })

# Quick Add Views (HTMX)
def add_designation_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Designation.objects.create(name=name)
        return HttpResponse('')

def add_department_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Department.objects.create(name=name)
        return HttpResponse('')

def add_staff_type_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            StaffType.objects.create(name=name)
        return HttpResponse('')

def teacher_list(request):
    teachers = TeacherProfile.objects.select_related('user', 'designation', 'department').all().order_by('-id')
    
    # ড্রপডাউনের জন্য মাস্টার ডেটা সংগ্রহ
    designations = Designation.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    staff_types = StaffType.objects.all().order_by('name')
    blood_groups = BloodGroup.objects.all().order_by('name')
    shifts = AcademicShift.objects.all().order_by('name')
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'teachers': teachers,
        'designations': designations,
        'departments': departments,
        'staff_types': staff_types,
        'blood_groups': blood_groups,
        'shifts': shifts,
        'subjects': subjects,
    }
    return render(request, 'teachers/teacher_list.html', context)

def add_teacher_htmx(request):
    if request.method == 'POST':
        # ১. ইউজার তৈরি
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.create_user(
            username=username, 
            password=password, 
            first_name=first_name, 
            last_name=last_name,
            role='teacher' # রোল অ্যাসাইন করা হলো
        )
        
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
            user.save()

        # ২. টিচার প্রোফাইল তৈরি (ডাইনামিক আইডি ব্যবহার করে)
        new_teacher = TeacherProfile.objects.create(
            user=user,
            employee_id=request.POST.get('employee_id'),
            designation_id=request.POST.get('designation_id'),
            department_id=request.POST.get('department_id'),
            staff_type_id=request.POST.get('staff_type_id'),
            shift_id=request.POST.get('shift_id'),
            blood_group_id=request.POST.get('blood_group_id'),
            qualification=request.POST.get('qualification'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            gender=request.POST.get('gender'),
            salary=request.POST.get('salary', 0),
        )

        # ৩. মেনি-টু-মেনি (Subjects) সেভ করা
        subject_ids = request.POST.getlist('subject_ids')
        if subject_ids:
            new_teacher.subjects.set(subject_ids)
        
        return render(request, 'teachers/partials/teacher_row.html', {'teacher': new_teacher})
    
def edit_teacher_htmx(request, pk):
    teacher = get_object_or_404(TeacherProfile, id=pk)
    
    # ড্রপডাউনের জন্য মাস্টার ডেটা সংগ্রহ
    designations = Designation.objects.all().order_by('name')
    departments = Department.objects.all().order_by('name')
    staff_types = StaffType.objects.all().order_by('name')
    blood_groups = BloodGroup.objects.all().order_by('name')
    shifts = AcademicShift.objects.all().order_by('name')
    subjects = Subject.objects.all().order_by('name')
    
    context = {
        'teacher': teacher,
        'designations': designations,
        'departments': departments,
        'staff_types': staff_types,
        'blood_groups': blood_groups,
        'shifts': shifts,
        'subjects': subjects,
    }
    return render(request, 'teachers/partials/teacher_edit_row.html', context)

def update_teacher_htmx(request, pk):
    teacher = get_object_or_404(TeacherProfile, id=pk)
    if request.method == 'POST':
        
        # ১. ইউজার ডেটা আপডেট
        user = teacher.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        user.save()

        # ২. টিচার প্রোফাইল আপডেট (Foreign Key ID ব্যবহার করে)
        teacher.employee_id = request.POST.get('employee_id')
        
        # ডাইনামিক ড্রপডাউনের আইডি
        teacher.designation_id = request.POST.get('designation_id') or None
        teacher.department_id = request.POST.get('department_id') or None
        teacher.staff_type_id = request.POST.get('staff_type_id') or None
        teacher.shift_id = request.POST.get('shift_id') or None
        teacher.blood_group_id = request.POST.get('blood_group_id') or None
        
        teacher.qualification = request.POST.get('qualification')
        teacher.phone_number = request.POST.get('phone_number')
        teacher.address = request.POST.get('address')
        teacher.gender = request.POST.get('gender')
        teacher.salary = request.POST.get('salary', 0)
        
        teacher.save()

        # ৩. Many-to-Many সাবজেক্ট আপডেট
        subject_ids = request.POST.getlist('subject_ids')
        if subject_ids:
            teacher.subjects.set(subject_ids)
        else:
            teacher.subjects.clear() # যদি কোনো সাবজেক্ট সিলেক্ট না করে

        return render(request, 'teachers/partials/teacher_row.html', {'teacher': teacher})

def delete_teacher(request, pk):
    if request.method == 'POST':
        teacher = TeacherProfile.objects.select_related('user').get(id=pk)
        user = teacher.user
        user.delete() # ইউজার ডিলিট হলে টিচার প্রোফাইলও স্বয়ংক্রিয়ভাবে ডিলিট হয়ে যাবে
        return HttpResponse('')

def filter_teachers_htmx(request):
    search_query = request.GET.get('search_query', '').strip()
    designation = request.GET.get('designation', '').strip()
    gender = request.GET.get('gender', 'all')
    shift = request.GET.get('shift', 'all')
    
    teachers = TeacherProfile.objects.select_related('user').all().order_by('-joining_date')
    
    if search_query:
        teachers = teachers.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query)
        )
    if designation:
        teachers = teachers.filter(designation__icontains=designation)
    if gender and gender != 'all':
        teachers = teachers.filter(gender=gender)
    if shift and shift != 'all':
        teachers = teachers.filter(shift=shift)
        
    return render(request, 'teachers/partials/teacher_table_body.html', {'teachers': teachers})