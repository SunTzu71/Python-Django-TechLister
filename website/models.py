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


class Experience(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, db_column='user_id')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_month = models.CharField(max_length=10)
    start_year = models.IntegerField(null=True, blank=True)
    end_month = models.CharField(max_length=10, null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    currently_working = models.BooleanField(default=False, null=True, blank=True)
    task_one = models.CharField(max_length=255, null=True, blank=True)
    task_two = models.CharField(max_length=255, null=True, blank=True)
    task_three = models.CharField(max_length=255, null=True, blank=True)
    task_four = models.CharField(max_length=255, null=True, blank=True)
    task_five = models.CharField(max_length=255, null=True, blank=True)
    task_six = models.CharField(max_length=255, null=True, blank=True)
    task_seven = models.CharField(max_length=255, null=True, blank=True)
    task_eight = models.CharField(max_length=255, null=True, blank=True)
    task_nine = models.CharField(max_length=255, null=True, blank=True)
    task_ten = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id} {self.company}'
