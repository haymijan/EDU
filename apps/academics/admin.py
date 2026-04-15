# File: apps/academics/admin.py
from django.contrib import admin
from .models import ClassRoom, Section, Subject

@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'classroom', 'shift', 'capacity')
    list_filter = ('shift', 'classroom')
    search_fields = ('name', 'classroom__name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'classroom', 'subject_type', 'full_marks')
    list_filter = ('subject_type', 'classroom')
    search_fields = ('name', 'code')