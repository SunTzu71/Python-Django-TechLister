from django.contrib import admin
from .models import PersonalInformation, Education, Experience, UserSkill


admin.site.register(PersonalInformation)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(UserSkill)
