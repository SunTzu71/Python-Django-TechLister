from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views


# message system is for users and recruiters
urlpatterns = [
    path('message/new/<int:user_id>', views.new_message, name='new_message'),
    path('message/reply/<int:msg_id>/<int:user_id>', views.reply_message, name='reply_message'),
    path('message/view/<int:msg_id>', views.view_message, name='view_message'),
    path('message/delete/<int:msg_id>', views.delete_message, name='delete_message'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)