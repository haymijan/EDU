# File: apps/students/urls.py

from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [

    # Setup Dashboard URLs
    
    path('', views.student_list, name='student_list'),
    path('add-htmx/', views.add_student_htmx, name='add_student_htmx'),
    path('<int:pk>/delete/', views.delete_student, name='delete_student'),

    path('<int:pk>/edit/', views.edit_student_htmx, name='edit_student'),
    path('<int:pk>/update/', views.update_student_htmx, name='update_student'),
    path('filter/', views.filter_students_htmx, name='filter_students'),


    path('setup/', views.student_setup_dashboard, name='student_setup'),
    path('setup/session/add/', views.add_session_quick, name='add_session_quick'),
    path('setup/category/add/', views.add_category_quick, name='add_category_quick'),
    path('setup/blood-group/add/', views.add_blood_group_quick, name='add_blood_group_quick'),
]