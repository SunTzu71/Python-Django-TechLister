from django.contrib import admin
from .models import PersonalInformation, Education, Experience, UserSkill, Portfolio


admin.site.register(PersonalInformation)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(UserSkill)
admin.site.register(Portfolio)
