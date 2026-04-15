# File: apps/academics/services.py

from .models import ClassRoom, Section

def create_classroom_service(name, campus, description=""):
    return ClassRoom.objects.create(name=name, campus=campus, description=description)

def update_classroom_service(classroom_id, name, campus, description=""):
    classroom = ClassRoom.objects.get(id=classroom_id)
    classroom.name = name
    classroom.campus = campus # নতুন যুক্ত হলো
    classroom.description = description
    classroom.save()
    return classroom