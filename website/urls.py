
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('add_personalinfo', views.add_personal_info, name='add_personalinfo'),
    path('add_education', views.add_education, name='add_education'),
    path('add_experience', views.add_experience, name='add_experience'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('recruiter_profile/', views.recruiter_profile, name='recruiter_profile')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
