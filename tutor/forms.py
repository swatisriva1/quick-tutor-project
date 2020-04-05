from django import forms
from .models import Profile, Subject, Job
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.forms import UserChangeForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit


class List(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email_addr", "phone_number", "subjects_can_help"]
        labels = {
            "email_addr": "Email address",
            "subjects_can_help": "Subjects you can tutor in" 
        }

    def __init__(self, *args, **kwargs):
        super(List, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'id-profile_form'
        self.helper.form_class = 'blueForms'
        self.helper.form_method = 'post'
        self.helper.form_action = 'update_profile'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('email_addr'),
            Field('phone_number'),
            Field('subjects_can_help', css_class="custom-select"),
            ButtonHolder(
                Submit('submit', 'Submit', css_class='btn btn-outline-primary')
            )
        )

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
