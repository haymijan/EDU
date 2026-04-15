# File: apps/academics/urls.py

from django.urls import path
from . import views

app_name = 'academics'

urlpatterns = [
    # Classrooms
    path('classrooms/', views.classroom_list, name='classroom_list'),
    path('classrooms/add/', views.add_classroom_htmx, name='add_classroom_htmx'),
    path('classrooms/filter/', views.filter_classrooms_htmx, name='filter_classrooms'),
    path('classrooms/<int:pk>/edit/', views.edit_classroom_htmx, name='edit_classroom'),
    path('classrooms/<int:pk>/update/', views.update_classroom_htmx, name='update_classroom'),
    path('classrooms/<int:pk>/delete/', views.delete_classroom, name='delete_classroom'),

    # Sections
    path('sections/', views.section_list, name='section_list'),
    path('sections/add/', views.add_section_htmx, name='add_section_htmx'),
    path('sections/filter/', views.filter_sections_htmx, name='filter_sections'),
    path('sections/<int:pk>/edit/', views.edit_section_htmx, name='edit_section'),
    path('sections/<int:pk>/update/', views.update_section_htmx, name='update_section'),
    path('sections/<int:pk>/delete/', views.delete_section, name='delete_section'),

    # Subjects
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/add/', views.add_subject_htmx, name='add_subject_htmx'),
    path('subjects/filter/', views.filter_subjects_htmx, name='filter_subjects'),
    path('subjects/<int:pk>/edit/', views.edit_subject_htmx, name='edit_subject'),
    path('subjects/<int:pk>/update/', views.update_subject_htmx, name='update_subject'),
    path('subjects/<int:pk>/delete/', views.delete_subject, name='delete_subject'),

    # Campus URLs
    path('campuses/', views.campus_list, name='campus_list'),
    path('campuses/add/', views.add_campus_htmx, name='add_campus_htmx'),
    path('campuses/<int:pk>/delete/', views.delete_campus, name='delete_campus'),

    # Quick Add for Group & Shift
    path('groups/add-quick/', views.add_group_quick, name='add_group_quick'),
    path('shifts/add-quick/', views.add_shift_quick, name='add_shift_quick'),

    path('setup/', views.academic_setup_dashboard, name='academic_setup'),
    path('setup/campus/add/', views.add_campus_quick, name='add_campus_quick'),
    path('setup/group/add/', views.add_group_quick, name='add_group_quick'),
    path('setup/shift/add/', views.add_shift_quick, name='add_shift_quick'),
]