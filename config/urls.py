# File: config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # হোম পেজ (সরাসরি http://127.0.0.1:8000/ এ গেলেই ড্যাশবোর্ড দেখা যাবে)
    path('', TemplateView.as_view(template_name='dashboard.html'), name='home'),
    
    # অ্যাপের ইউআরএলগুলো (Namespace সহ)
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('students/', include('apps.students.urls', namespace='students')),
    path('academics/', include('apps.academics.urls', namespace='academics')),
    path('teachers/', include('apps.teachers.urls', namespace='teachers')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)