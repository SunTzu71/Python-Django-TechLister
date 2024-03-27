
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),

    # login register
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    # section where user and recruiter can visit
    path('add/personalinfo', views.add_personal_info, name='add_personalinfo'),
    path('edit/personalinfo/<int:pk>', views.edit_personal_info, name='edit_personalinfo'),
    path('resume/<int:pk>', views.user_resume, name='user_resume'),

    # user section
    path('user/profile/', views.user_profile, name='user_profile'),
    path('user/add/education/', views.add_education, name='add_education'),
    path('user/edit/education/<int:pk>', views.edit_education, name='edit_education'),
    path('user/delete/education/<int:pk>', views.delete_education, name='delete_education'),
    path('user/add/experience', views.add_experience, name='add_experience'),
    path('user/edit/experience/<int:pk>', views.edit_experience, name='edit_experience'),
    path('user/delete/experience/<int:pk>', views.delete_experience, name='delete_experience'),
    path('user/portfolio/add', views.add_portfolio, name='add_user_portfolio'),
    path('user/portfolio/edit/<int:pk>', views.edit_portfolio, name='edit_portfolio'),
    path('user/portfolio/delete/<int:pk>', views.delete_portfolio, name='delete_portfolio'),

    # recruiter section
    path('recruiter/profile/', views.recruiter_profile, name='recruiter_profile'),
    path('recruiter/job/listing/add/skill', views.add_job_skill, name='add_job_skill'),
    path('recruiter/job/listing/add', views.add_job, name='add_job'),
    path('recruiter/job/listing/edit/<int:pk>', views.edit_job, name='edit_job'),
    path('recruiter/job/listing/delete/<int:pk>', views.delete_job, name='delete_job'),
    path('job/listing/<int:pk>', views.view_job, name='view_job'),

    # skill / user skill / job skill
    path('skill_search/', views.skill_search, name='skill_search'),
    path('add_skill/<str:skill_input>', views.add_skill, name='add_skill'),
    path('add_user_skill/<int:pk>/<str:skill_name>', views.add_user_skill, name='add_user_skill'),
    path('delete_user_skilil/<int:pk>', views.delete_user_skill, name='delete_user_skill'),
    path('delete_job_skilil/<int:pk>', views.delete_job_skill, name='delete_job_skill'),

    # job search
    path('job/search/', views.job_search, name='job_search'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
