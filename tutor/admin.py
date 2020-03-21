from django.contrib import admin
from .models import Profile, Subject, Job

# Register your models here.
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Job)