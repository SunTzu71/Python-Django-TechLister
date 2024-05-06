from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


# message system is for users and recruiters
urlpatterns = [
    path('user/ai/resume', views.ai_resume, name='ai_resume'),

    # ai resume section
    path('get/about/info', views.get_about_info, name='get_about_info'),
    path('get/ai/experience', views.get_ai_experience, name='get_ai_experience'),

    # skills section
    path('get/skills/list', views.get_skill_list, name='get_skill_list'),
    path('ai/skill/delete/<int:skill_id>', views.ai_skill_delete, name='ai_skill_delete'),
    path('ai/skill/add', views.ai_skill_add, name='ai_skill_add'),
    path('add/skill/cancel', views.add_skill_cancel, name='add_skill_cancel'),

    # education section
    path('get/education/list', views.get_education_list, name='get_education_list'),
    path('ai/add/education/', views.ai_add_education, name='ai_add_education'),
    path('add/education/submit', views.add_education_submit, name='add_education_submit'),
    path('add/education/cancel', views.add_education_cancel, name='add_education_cancel'),
    path('delete/education/<int:pk>', views.delete_education, name='delete_education'),
    path('ai/edit/education/<int:pk>', views.ai_edit_education, name='ai_edit_education'),
    path('edit/education/submit/<int:pk>', views.edit_education_submit, name='edit_education_submit'),
    path('edit/education/cancel/<int:pk>', views.edit_education_cancel, name='edit_education_cancel'),

    # experience section
    path('get/experience/list', views.get_experience_list, name='get_experience_list'),
    path('add/experience/submit', views.add_experience_submit, name='add_experience_submit'),
    path('add/experience/cancel', views.add_experience_cancel, name='add_experience_cancel'),
    path('ai/delete/experience/<int:pk>', views.ai_delete_experience, name='ai_delete_experience'),
    path('edit/experience/submit/<int:pk>', views.edit_experience_submit, name='edit_experience_submit'),
    path('edit/experience/cancel/<int:pk>', views.edit_experience_cancel, name='edit_experience_cancel'),

    # AI section
    path('ai/about/me', views.ai_about_me, name='ai_about_me'),
    path('ai/about/update', views.ai_about_update, name='ai_about_update'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
