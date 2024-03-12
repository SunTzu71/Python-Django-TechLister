from django.contrib.auth.models import User
from django.db import models


class PersonalInformation(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, db_column='user_id')
    recruiter = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    linked_in = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    about = models.TextField()
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Education(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, db_column='user_id')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id} {self.title}'

