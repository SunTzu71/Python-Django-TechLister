from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


# message system is for users and recruiters
urlpatterns = [
    path('user/ai/resume', views.ai_resume, name='ai_resume'),
    path('user/ai/edit/education/<int:pk>', views.ai_edit_education, name='ai_edit_education'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
