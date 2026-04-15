# File: apps/accounts/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]