from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


# message system is for users and recruiters
urlpatterns = [
    path('user/ai/resume', views.ai_resume, name='ai_resume'),
    path('get/education/list', views.get_education_list, name='get_education_list'),
    path('ai/add/education/', views.ai_add_education, name='ai_add_education'),
    path('add/education/submit', views.add_education_submit, name='add_education_submit'),
    path('add/education/cancel', views.add_education_cancel, name='add_education_cancel'),
    path('delete/education/<int:pk>', views.delete_education, name='delete_education'),
    path('ai/edit/education/<int:pk>', views.ai_edit_education, name='ai_edit_education'),
    path('edit/education/submit/<int:pk>', views.edit_education_submit, name='edit_education_submit'),
    path('edit/education/cancel/<int:pk>', views.edit_education_cancel, name='edit_education_cancel'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
