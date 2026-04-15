# File: apps/accounts/views.py

from django.shortcuts import render, redirect # 'render' ইম্পোর্ট করা হলো
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import role_required
from apps.students.models import Student

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return reverse_lazy('accounts:admin_dashboard')
        elif user.role == 'TEACHER':
            return reverse_lazy('accounts:teacher_dashboard')
        elif user.role == 'STUDENT':
            return reverse_lazy('accounts:student_dashboard')
        return reverse_lazy('home')

@login_required
@role_required(allowed_roles=['ADMIN'])
def admin_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
    }
    return render(request, 'accounts/admin_dashboard.html', context) # এখন আর এরর আসবে না

# এই ফাংশনটি আপনার ফাইলে মিসিং ছিল
@login_required
@role_required(allowed_roles=['STUDENT'])
def student_dashboard(request):
    return render(request, 'accounts/student_dashboard.html')

# টিচার ড্যাশবোর্ডও যোগ করে রাখুন ভবিষ্যতে এরর এড়াতে
@login_required
@role_required(allowed_roles=['TEACHER'])
def teacher_dashboard(request):
    return render(request, 'accounts/teacher_dashboard.html')