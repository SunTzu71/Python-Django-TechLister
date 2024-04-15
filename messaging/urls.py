from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('new/message', views.new_message, name='new_message'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)