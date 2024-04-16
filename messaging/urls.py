from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('new/message/<int:user_id>', views.new_message, name='new_message'),
    path('user/view/<int:msg_id>', views.view_message, name='view_message'),
    path('user/delete/<int:msg_id>', views.delete_message, name='delete_message'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)