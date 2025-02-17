
from django.urls import path, include
from . import views
from .allviews import verify_user_email
from .allviews import users
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('please/login/', views.login_page, name='login_page'),
    path('restricted/access/', views.restricted_access, name='restricted_access'),
    path('summernote/', include('django_summernote.urls')),

    # job seeker and business recruiter funnel page
    path('job/seeker/', views.job_seeker, name='job_seeker'),
    path('business/recruiter/', views.business_recruiter, name='business_recruiter'),

    # login register
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('verify/<slug:uidb64>/<slug:token>/', verify_user_email.verify_email, name='verify_email'),
    path('verify/success/', verify_user_email.verification_success, name='verification_success'),
    path('verify/failure/', verify_user_email.verification_failure, name='verification_failure'),
    path('verify/email/', views.check_email_verify, name='check_email_verify'),

    # password reset
    # Class based view passes in the form directly for us so we can use it in the template
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="reset.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="reset_password_complete.html"),
         name='password_reset_complete'),

    # section where user and recruiter can visit
    path('add/personalinfo', views.add_personal_info, name='add_personalinfo'),
    path('edit/personalinfo/<int:pk>', views.edit_personal_info, name='edit_personalinfo'),

    # user section
    path('user/profile/', users.user_profile, name='user_profile'),
    path('user/delete/profile/image', views.delete_profile_image, name='delete_profile_image'),
    path('user/add/education/', views.add_education, name='add_education'),
    path('user/edit/education/<int:pk>', views.edit_education, name='edit_education'),
    path('user/delete/education/<int:pk>', views.delete_education, name='delete_education'),
    path('user/add/experience', views.add_experience, name='add_experience'),
    path('user/edit/experience/<int:pk>', views.edit_experience, name='edit_experience'),
    path('user/delete/experience/<int:pk>', views.delete_experience, name='delete_experience'),
    path('user/portfolio/add', views.add_portfolio, name='add_user_portfolio'),
    path('user/portfolio/edit/<int:pk>', views.edit_portfolio, name='edit_portfolio'),
    path('user/portfolio/delete/<int:pk>', views.delete_portfolio, name='delete_portfolio'),
    path('user/apply/job/<int:pk>', views.apply_job, name='apply_job'),
    path('user/ai/coverletter/<int:pk>', views.ai_cover_letter, name='ai_cover_letter'),
    path('user/manual/coverletter/<int:pk>', views.manual_cover_letter, name='manual_cover_letter'),
    path('user/applied/remove/job/<int:pk>', views.remove_applied_job, name='remove_applied_job'),
    path('user/remove/job/<int:pk>', views.user_profile_remove_job, name='user_profile_remove_job'),
    path('user/saved/jobs', users.saved_jobs, name='saved_jobs'),
    path('user/applied/jobs', users.applied_jobs, name='applied_jobs'),
    path('user/edit/resume', users.edit_resume, name='edit_resume'),
    path('user/ai/info', users.ai_info, name='ai_info'),

    # recruiter section

    path('recruiter/job/listing/delete/<int:pk>', views.delete_job, name='delete_job'),
    path('recruiter/profile/remove/resume/<int:pk>', views.rec_remove_resume, name='rec_remove_resume'),
    path('recruiter/view_cover_letter/<int:jobid>/<int:userid>', views.view_cover_letter, name='view_cover_letter'),
    path('recruiter/delete/applied/<int:jobid>/<int:userid>', views.rec_delete_applied, name='rec_delete_applied'),

    # skill / user skill / job skill
    path('skill_search/', views.skill_search, name='skill_search'),
    path('add_skill/<str:skill_input>', views.add_skill, name='add_skill'),
    path('add_user_skill/<int:pk>/<str:skill_name>', views.add_user_skill, name='add_user_skill'),
    path('delete_user_skilil/<int:pk>', views.delete_user_skill, name='delete_user_skill'),
    path('delete_job_skilil/<int:pk>', views.delete_job_skill, name='delete_job_skill'),

    # job user search - look into removing job and user search and keep search
    path('search/', views.main_search, name='main_search'),
    path('job/search/', views.job_search, name='job_search'),
    path('user2/search/', views.user_search, name='user_search'),

    # job user save and remove
    path('job/save/<int:pk>', views.save_job, name='save_job'),
    path('job/remove/<int:pk>', views.remove_job, name='remove_job'),
    path('job/listing/<int:pk>', views.view_job, name='view_job'),
    path('user2/save/<int:pk>', views.save_user, name='save_user'),
    path('user2/remove/<int:pk>', views.remove_user, name='remove_user'),
    path('all/job/<int:pk>', views.all_view_job, name='all_view_job'),

    # resume and user page
    path('resume/<int:pk>', views.user_resume, name='user_resume'),
    path('all/resume/<int:pk>', views.all_resume, name='all_resume'),
    path('resume/<str:username>', views.user_page, name='user_page'),
    path('portfolio/<str:username>', views.user_portfolio, name='user_portfolio'),

    # Article add edit view
    path('article/add', views.add_article, name='add_article'),
    path('article/edit/<int:pk>', views.edit_article, name='edit_article'),
    path('article/list/', views.list_articles, name='list_articles'),
    path('article/view/<int:pk>', views.view_article, name='view_article'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
