from django.contrib import admin
from .models import PersonalInformation, Education, Experience


admin.site.register(PersonalInformation)
admin.site.register(Education)
admin.site.register(Experience)
