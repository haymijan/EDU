# File: apps/academics/models.py

from django.db import models

#=============================================================

# ১. নতুন ডাইনামিক ক্যাম্পাস মডেল
class Campus(models.Model):
    name = models.CharField(max_length=100, unique=True) # যেমন: General Campus
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ২. আপডেট করা ক্লাসরুম মডেল
class ClassRoom(models.Model):
    # এখন এটি ফিক্সড কোডের বদলে সরাসরি Campus মডেলের সাথে যুক্ত (ForeignKey)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE, related_name='classrooms')
    
    name = models.CharField(max_length=50) 
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'campus')

    def __str__(self):
        return f"{self.name} ({self.campus.name})"
    
# ১. নতুন ডাইনামিক শিফট মডেল
class AcademicShift(models.Model):
    name = models.CharField(max_length=50, unique=True) # যেমন: Morning, Day, Evening

    def __str__(self):
        return self.name

# ২. নতুন ডাইনামিক গ্রুপ মডেল
class AcademicGroup(models.Model):
    name = models.CharField(max_length=50, unique=True) # যেমন: General, Science, Arts

    def __str__(self):
        return self.name

# ৩. আপডেট করা Section মডেল
class Section(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='sections')
    name = models.CharField(max_length=50) # যেমন: A, B, Padma
    
    # ফিক্সড choices মুছে ফেলে ForeignKey করা হলো:
    group = models.ForeignKey(AcademicGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='sections')
    shift = models.ForeignKey(AcademicShift, on_delete=models.SET_NULL, null=True, blank=True, related_name='sections')
    
    capacity = models.IntegerField(default=50)
    room_number = models.CharField(max_length=20, blank=True, null=True)
    class_teacher = models.ForeignKey('teachers.TeacherProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='class_sections')

    class Meta:
        unique_together = ('name', 'classroom', 'shift') 

    def __str__(self):
        shift_name = self.shift.name if self.shift else "No Shift"
        return f"{self.classroom.name} - {self.name} ({shift_name})"

class Subject(models.Model):
    SUBJECT_TYPES = (
        ('core', 'Core / Mandatory'),
        ('elective', 'Elective / Optional'),
    )
    name = models.CharField(max_length=100) # যেমন: Mathematics, Higher Math
    code = models.CharField(max_length=20, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='subjects')
    subject_type = models.CharField(max_length=20, choices=SUBJECT_TYPES, default='core')
    full_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=33)

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.classroom.name}"