from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


# message system is for users and recruiters
urlpatterns = [
    path('recruiter/job/listing/add', views.add_job, name='add_job'),
    path('recruiter/profile/', views.recruiter_profile, name='recruiter_profile'),
    path('recruiter/applications/', views.user_applications, name='user_applications'),
    path('recruiter/job/listings', views.job_listings, name='job_listings'),
    path('recruiter/saved/resumes', views.saved_resumes, name='saved_resumes'),

    path('job/skill/add', views.job_skill_add, name='job_skill_add'),
    path('recruiter/job/listing/edit/<int:pk>', views.edit_job, name='edit_job'),
    path('get/job/skills', views.get_job_skills, name='get_job_skills'),
    path('get/session/skills/<int:job_id>', views.get_session_skills, name='get_session_skills'),
    path('job/skill/delete/<str:skill_name>', views.job_skill_delete, name='job_skill_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
