# File: apps/academics/views.py

from django.shortcuts import render, get_object_or_404
from .models import ClassRoom, Section, Subject, Campus, AcademicGroup, AcademicShift
from django.http import HttpResponse
from .services import update_classroom_service
from apps.teachers.models import TeacherProfile

# ================= ACADEMIC SETUP DASHBOARD =================
def academic_setup_dashboard(request):
    campuses = Campus.objects.all().order_by('name')
    groups = AcademicGroup.objects.all().order_by('name')
    shifts = AcademicShift.objects.all().order_by('name')
    
    return render(request, 'academics/setup_dashboard.html', {
        'campuses': campuses,
        'groups': groups,
        'shifts': shifts
    })

def add_campus_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address', '')
        if name:
            Campus.objects.create(name=name, address=address)
        return HttpResponse('') # HTMX অটোমেটিক পেজ রিলোড করবে

def add_group_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AcademicGroup.objects.create(name=name)
        return HttpResponse('')

def add_shift_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AcademicShift.objects.create(name=name)
        return HttpResponse('')

# ================= CAMPUS VIEWS =================
def campus_list(request):
    campuses = Campus.objects.all().order_by('name')
    return render(request, 'academics/campus_list.html', {'campuses': campuses})

def add_campus_htmx(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        new_campus = Campus.objects.create(name=name, address=address)
        return render(request, 'academics/partials/campus_row.html', {'campus': new_campus})

def delete_campus(request, pk):
    if request.method == 'POST':
        Campus.objects.get(id=pk).delete()
        return HttpResponse('')

# ================= CLASSROOM VIEWS =================
def classroom_list(request):
    classrooms = ClassRoom.objects.select_related('campus').prefetch_related('sections').all().order_by('name')
    campuses = Campus.objects.all().order_by('name') # ডাটাবেস থেকে ডাইনামিক ক্যাম্পাস আনা হচ্ছে
    return render(request, 'academics/classroom_list.html', {
        'classrooms': classrooms, 
        'campuses': campuses
    })

def add_classroom_htmx(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        campus_id = request.POST.get('campus_id') # ফর্ম থেকে campus_id রিসিভ করা
        description = request.POST.get('description')
      
        new_class = ClassRoom.objects.create(
            name=name, 
            campus_id=campus_id, # ডাটাবেসে সেভ করা
            description=description
        )
        return render(request, 'academics/partials/classroom_row.html', {'classroom': new_class})
    
def edit_classroom_htmx(request, pk):
    classroom = get_object_or_404(ClassRoom, id=pk)
    campuses = Campus.objects.all().order_by('name') # এডিট ফর্মে দেখানোর জন্য
    return render(request, 'academics/partials/classroom_edit_row.html', {
        'classroom': classroom, 
        'campuses': campuses
    })

def delete_classroom(request, pk):
    if request.method == 'POST':
        ClassRoom.objects.get(id=pk).delete()
        return HttpResponse('')

def update_classroom_htmx(request, pk):
    if request.method == 'POST':
        classroom = get_object_or_404(ClassRoom, id=pk)
        classroom.name = request.POST.get('name')
        classroom.campus_id = request.POST.get('campus_id') # আপডেট
        classroom.description = request.POST.get('description')
        classroom.save()
        return render(request, 'academics/partials/classroom_row.html', {'classroom': classroom})

def filter_classrooms_htmx(request):
    search_query = request.GET.get('search_query', '').strip()
    campus_filter = request.GET.get('campus', 'all')
    
    classrooms = ClassRoom.objects.select_related('campus').all().order_by('name')
    
    if search_query:
        classrooms = classrooms.filter(name__icontains=search_query)
        
    if campus_filter and campus_filter != 'all':
        classrooms = classrooms.filter(campus_id=campus_filter)
        
    return render(request, 'academics/partials/classroom_table_body.html', {'classrooms': classrooms})

# ================= SECTION VIEWS =================
def section_list(request):
    sections = Section.objects.select_related('classroom__campus', 'group', 'shift', 'class_teacher__user').all().order_by('classroom__name', 'name')
    classrooms = ClassRoom.objects.select_related('campus').all().order_by('name')
    teachers = TeacherProfile.objects.select_related('user').all().order_by('user__first_name')
    
    groups = AcademicGroup.objects.all().order_by('name')
    shifts = AcademicShift.objects.all().order_by('name')
    
    context = {
        'sections': sections, 
        'classrooms': classrooms, 
        'teachers': teachers,
        'groups': groups,
        'shifts': shifts
    }
    return render(request, 'academics/section_list.html', context)

def add_section_htmx(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('class_teacher_id')
        group_id = request.POST.get('group_id')
        shift_id = request.POST.get('shift_id')
        
        new_section = Section.objects.create(
            classroom_id=request.POST.get('classroom_id'),
            name=request.POST.get('name'),
            group_id=group_id if group_id else None,
            shift_id=shift_id if shift_id else None,
            capacity=request.POST.get('capacity', 50),
            room_number=request.POST.get('room_number'),
            class_teacher_id=teacher_id if teacher_id else None
        )
        return render(request, 'academics/partials/section_row.html', {'section': new_section})

def delete_section(request, pk):
    if request.method == 'POST':
        Section.objects.get(id=pk).delete()
        return HttpResponse('')

def filter_sections_htmx(request):
    classroom_id = request.GET.get('classroom')
    sections = Section.objects.select_related('classroom__campus', 'group', 'shift', 'class_teacher__user').all().order_by('classroom__name', 'name')
    if classroom_id and classroom_id != 'all':
        sections = sections.filter(classroom_id=classroom_id)
    return render(request, 'academics/partials/section_table_body.html', {'sections': sections})

def edit_section_htmx(request, pk):
    section = get_object_or_404(Section, id=pk)
    classrooms = ClassRoom.objects.select_related('campus').all().order_by('name')
    teachers = TeacherProfile.objects.select_related('user').all().order_by('user__first_name')
    groups = AcademicGroup.objects.all().order_by('name')
    shifts = AcademicShift.objects.all().order_by('name')
    
    return render(request, 'academics/partials/section_edit_row.html', {
        'section': section, 
        'classrooms': classrooms, 
        'teachers': teachers,
        'groups': groups,
        'shifts': shifts
    })

def update_section_htmx(request, pk):
    section = get_object_or_404(Section, id=pk)
    if request.method == 'POST':
        section.classroom_id = request.POST.get('classroom_id')
        section.name = request.POST.get('name')
        
        group_id = request.POST.get('group_id')
        section.group_id = group_id if group_id else None
        
        shift_id = request.POST.get('shift_id')
        section.shift_id = shift_id if shift_id else None
        
        section.capacity = request.POST.get('capacity', 50)
        section.room_number = request.POST.get('room_number')
        
        teacher_id = request.POST.get('class_teacher_id')
        section.class_teacher_id = teacher_id if teacher_id else None
        
        section.save()
        return render(request, 'academics/partials/section_row.html', {'section': section})

# ================= SUBJECT VIEWS =================
def subject_list(request):
    # ডাটাবেস থেকে সাবজেক্ট এবং ক্লাসের সাথে ক্যাম্পাসের ডেটাও আনা হচ্ছে
    subjects = Subject.objects.select_related('classroom__campus').all().order_by('classroom__name', 'name')
    classrooms = ClassRoom.objects.select_related('campus').all().order_by('name')
    return render(request, 'academics/subject_list.html', {'subjects': subjects, 'classrooms': classrooms})

def add_subject_htmx(request):
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        name = request.POST.get('name')
        code = request.POST.get('code')
        subject_type = request.POST.get('subject_type', 'core')
        full_marks = request.POST.get('full_marks', 100)
        pass_marks = request.POST.get('pass_marks', 33)

        # কোন ক্লাসের সাবজেক্ট সেটি বের করা
        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        
        # ডাটাবেসে সেভ করা
        new_subject = Subject.objects.create(
            classroom=classroom,
            name=name,
            code=code,
            subject_type=subject_type,
            full_marks=full_marks,
            pass_marks=pass_marks
        )
        return render(request, 'academics/partials/subject_row.html', {'subject': new_subject})

def delete_subject(request, pk):
    if request.method == 'POST':
        Subject.objects.get(id=pk).delete()
        return HttpResponse('')
    
def filter_subjects_htmx(request):
    search_query = request.GET.get('search_query', '').strip()
    subjects = Subject.objects.all().order_by('code')
    if search_query:
        subjects = subjects.filter(name__icontains=search_query) | subjects.filter(code__icontains=search_query)
    return render(request, 'academics/partials/subject_table_body.html', {'subjects': subjects})

def edit_subject_htmx(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    return render(request, 'academics/partials/subject_edit_row.html', {'subject': subject})

def update_subject_htmx(request, pk):
    subject = get_object_or_404(Subject, id=pk)
    if request.method == 'POST':
        subject.name = request.POST.get('name')
        subject.code = request.POST.get('code')
        subject.save()
        return render(request, 'academics/partials/subject_row.html', {'subject': subject})

# File: apps/academics/views.py

def add_group_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AcademicGroup.objects.create(name=name)
        return HttpResponse('') # HTMX অটোমেটিক পেজ রিলোড করে দেবে

def add_shift_quick(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            AcademicShift.objects.create(name=name)
        return HttpResponse('')