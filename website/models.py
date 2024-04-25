from django.contrib.auth.models import User
from django.db import models
from django_summernote.fields import SummernoteTextField


class PersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personal_information')
    recruiter = models.BooleanField(default=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    linked_in = models.URLField(null=True, blank=True)
    about = SummernoteTextField()
    profile_image = models.ImageField(null=True, blank=True, upload_to='images/', default='images/default-profile.jpeg')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Article(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, related_name='article')
    title = models.CharField(max_length=255)
    description = SummernoteTextField()
    draft = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.title}'


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, related_name='portfolios')
    title = models.CharField(max_length=255)
    description = models.TextField()
    website_link = models.URLField()
    portfolio_image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.title}'


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, related_name='education')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user} {self.title}'


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True, related_name='experience')
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_month = models.CharField(max_length=10)
    start_year = models.IntegerField()
    end_month = models.CharField(max_length=10, null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    currently_working = models.BooleanField(default=False, null=True, blank=True)
    task_one = models.CharField(max_length=255)
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
        return f'{self.user} {self.company}'


class Skill(models.Model):
    name = models.CharField(max_length=50)


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_constraint=True)
    skill_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'skill'),)

    def __str__(self):
        return f'{self.user.username} {self.skill_name}'


class JobListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_constraint=True)
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    job_type = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    pay_bottom = models.IntegerField(null=True, blank=True)
    pay_top = models.IntegerField(null=True, blank=True)
    description = SummernoteTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.title}'


class AppliedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    cover_letter = SummernoteTextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedJobs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class SavedUsers(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recruiter')
    saved = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')

    class Meta:
        unique_together = ('recruiter', 'saved')


class JobSkill(models.Model):
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE, db_constraint=True)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, db_constraint=True)
    skill_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job} {self.skill} {self.skill_name}'


class AIToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField(null=True, blank=True, default=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username + ' - ' + str(self.amount)
