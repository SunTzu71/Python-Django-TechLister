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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
