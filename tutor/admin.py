from django.contrib import admin
from .models import Profile, Subject, Job

# Register your models here.
admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Job)
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

