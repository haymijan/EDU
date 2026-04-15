# File: apps/students/views.py

from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from apps.academics.models import ClassRoom, Section
from .services import create_student_service
from .services import update_student_service

from .models import AcademicSession, AdmissionCategory, BloodGroup

from django.contrib.auth import get_user_model
User = get_user_model()

#===========================================================

def student_list(request):
    students = Student.objects.select_related('user', 'classroom__campus').all().order_by('-id')
    classrooms = ClassRoom.objects.select_related('campus').all().order_by('name')
    
    # নতুন যুক্ত করা হলো: ডাইনামিক সেশন এবং ক্যাটাগরি
    sessions = AcademicSession.objects.all().order_by('-name')
    categories = AdmissionCategory.objects.all().order_by('name')
    blood_groups = BloodGroup.objects.all().order_by('name')
    
    return render(request, 'students/student_list.html', {
        'students': students, 
        'classrooms': classrooms,
        'sessions': sessions,        # <--- যুক্ত করা হলো
        'categories': categories,     # <--- যুক্ত করা হলো
        'blood_groups': blood_groups
    })

def add_student_htmx(request):
    if request.method == 'POST':
        # ১. ইউজার ডেটা রিসিভ ও ইউজার তৈরি
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        
        # ছবি আপলোড থাকলে সেভ করা
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
            user.save()

        # ২. স্টুডেন্ট ও মাস্টার ডেটা রিসিভ
        roll_number = request.POST.get('roll_number')
        classroom_id = request.POST.get('classroom_id')
        session_id = request.POST.get('session_id')           # নতুন
        category_id = request.POST.get('category_id')         # নতুন
        blood_group_id = request.POST.get('blood_group_id')   # নতুন
        gender = request.POST.get('gender')
        
        # ৩. অভিভাবকের তথ্য রিসিভ
        guardian_name = request.POST.get('guardian_name')
        guardian_phone = request.POST.get('guardian_phone')
        guardian_email = request.POST.get('guardian_email')
        emergency_contact = request.POST.get('emergency_contact')
        guardian_address = request.POST.get('guardian_address')

        # ৪. ডাটাবেসে স্টুডেন্ট সেভ করা
        new_student = Student.objects.create(
            user=user,
            roll_number=roll_number,
            classroom_id=classroom_id,
            session_id=session_id if session_id else None,
            category_id=category_id if category_id else None,
            blood_group_id=blood_group_id if blood_group_id else None,
            gender=gender,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone,
            guardian_email=guardian_email,
            emergency_contact=emergency_contact,
            guardian_address=guardian_address
        )
        
        return render(request, 'students/partials/student_row.html', {'student': new_student})

def edit_student_htmx(request, pk):
    student = Student.objects.get(id=pk)
    classrooms = ClassRoom.objects.select_related('campus').all()
    sections = Section.objects.all()
    context = {
        'student': student,
        'classrooms': classrooms,
        'sections': sections
    }
    # এটি একটি নতুন পার্শিয়াল টেমপ্লেট যা আমরা পরের ধাপে তৈরি করব
    return render(request, 'students/partials/student_edit_row.html', context)

def update_student_htmx(request, pk):
    if request.method == 'POST':
        data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'roll_number': request.POST.get('roll_number'),
            'gender': request.POST.get('gender'),
            'classroom_id': request.POST.get('classroom'),
            'section_id': request.POST.get('section'),
            'guardian_phone': request.POST.get('guardian_phone'),
            'guardian_address': request.POST.get('guardian_address'),
            'profile_picture': request.FILES.get('profile_picture'),
        }
        
        updated_student = update_student_service(pk, data)
        # সেভ হওয়ার পর আবার সাধারণ রো রেন্ডার করবে
        return render(request, 'students/partials/student_row.html', {'student': updated_student})

def delete_student(request, pk):
    if request.method == 'POST':
        student = Student.objects.select_related('user').get(id=pk)
        user = student.user
        user.delete() 
        return HttpResponse('')

def filter_students_htmx(request):
    # ফ্রন্টএন্ড থেকে পাঠানো ডেটা রিসিভ করা
    classroom_id = request.GET.get('classroom')
    section_id = request.GET.get('section')
    gender = request.GET.get('gender')

    # প্রথমে সব স্টুডেন্ট সিলেক্ট করা
    students = Student.objects.select_related('user', 'classroom', 'section').all().order_by('-created_at')

    # ফিল্টার কন্ডিশন (যদি 'all' না হয়ে নির্দিষ্ট কোনো আইডি বা ভ্যালু আসে)
    if classroom_id and classroom_id != 'all':
        students = students.filter(classroom_id=classroom_id)
        
    if section_id and section_id != 'all':
        students = students.filter(section_id=section_id)
        
    if gender and gender != 'all':
        students = students.filter(gender=gender)

    # শুধুমাত্র নতুন টেবিল বডিটুকু রেন্ডার করে পাঠানো হচ্ছে
    return render(request, 'students/partials/student_table_body.html', {'students': students})

# Setup Dashboard View
def student_setup_dashboard(request):
    sessions = AcademicSession.objects.all().order_by('-name')
    categories = AdmissionCategory.objects.all().order_by('name')
    blood_groups = BloodGroup.objects.all().order_by('name') # নতুন যুক্ত হলো
    return render(request, 'students/setup_dashboard.html', {
        'sessions': sessions,
        'categories': categories,
        'blood_groups': blood_groups # পাঠানো হলো
    })

def add_blood_group_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            BloodGroup.objects.create(name=name)
        return HttpResponse('')

# Quick Add Views
def add_session_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AcademicSession.objects.create(name=name)
        return HttpResponse('') # HTMX পেজ রিলোড করবে

def add_category_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AdmissionCategory.objects.create(name=name)
        return HttpResponse('')