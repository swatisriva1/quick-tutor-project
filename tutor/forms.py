from django import forms
from .models import Profile
from django.contrib.auth.forms import UserChangeForm

class List(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email_addr", "phone_number"]

class EditProfile(UserChangeForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email_addr", "phone_number"]