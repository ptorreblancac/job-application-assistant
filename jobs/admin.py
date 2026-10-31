from django.contrib import admin
from .models import Job, SearchProfile, ProfileJobMatch

admin.site.register(Job)
admin.site.register(SearchProfile)
admin.site.register(ProfileJobMatch)