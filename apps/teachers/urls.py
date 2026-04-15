# File: apps/teachers/urls.py

from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teacher_list, name='teacher_list'),
    path('add/', views.add_teacher_htmx, name='add_teacher_htmx'),
    path('filter/', views.filter_teachers_htmx, name='filter_teachers'),
    path('<int:pk>/edit/', views.edit_teacher_htmx, name='edit_teacher'),
    path('<int:pk>/update/', views.update_teacher_htmx, name='update_teacher'),
    path('<int:pk>/delete/', views.delete_teacher, name='delete_teacher'),

    # ================= HR & TEACHER SETUP =================
    path('setup/', views.hr_setup_dashboard, name='hr_setup'),
    path('setup/designation/add/', views.add_designation_quick, name='add_designation_quick'),
    path('setup/department/add/', views.add_department_quick, name='add_department_quick'),
    path('setup/staff-type/add/', views.add_staff_type_quick, name='add_staff_type_quick'),
]