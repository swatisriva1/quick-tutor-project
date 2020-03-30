from django import forms
from .models import Profile, Subject, Job
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserChangeForm

class List(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email_addr", "phone_number", "subjects_can_help"]
        labels = {
            "email_addr": "Email address",
            "subjects_can_help": "Subjects you can tutor in" 
        } 

class PicForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["pic"]
        labels = {
            "pic": "Profile picture"
        }      

class EditProfile(UserChangeForm):
    class Meta:
        fields = ["first_name", "last_name", "email_addr", "phone_number", "subjects_can_help"]

class RequestTutor(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["subject", "course", "location", "notes"]

class AvailableJobs(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["subject", "course", "location", "notes"]
