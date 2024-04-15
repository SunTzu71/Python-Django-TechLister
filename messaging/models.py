from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_messages')
    subject = models.CharField(max_length=100)
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class MessageReply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='+')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_reply_messages')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_reply_messages')
    body = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)