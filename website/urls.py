
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

    # user profile
    path('user_profile/', views.user_profile, name='user_profile'),
    path('add_personalinfo', views.add_personal_info, name='add_personalinfo'),
    path('edit_personalinfo/<int:pk>', views.edit_personal_info, name='edit_personalinfo'),
    path('add_education/', views.add_education, name='add_education'),
    path('edit_education/<int:pk>', views.edit_education, name='edit_education'),
    path('delete_education/<int:pk>', views.delete_education, name='delete_education'),
    path('add_experience', views.add_experience, name='add_experience'),
    path('edit_experience/<int:pk>', views.edit_experience, name='edit_experience'),
    path('delete_experience/<int:pk>', views.delete_experience, name='delete_experience'),

    # recruiter profile
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile'),


    # skill / user skill
    path('skill_search/', views.skill_search, name='skill_search'),
    path('add_skill/<str:skill_input>', views.add_skill, name='add_skill'),
    path('add_user_skill/<int:pk>/<str:skill_name>', views.add_user_skill, name='add_user_skill'),
    path('delete_user_skilil/<int:pk>', views.delete_user_skill, name='delete_user_skill'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
