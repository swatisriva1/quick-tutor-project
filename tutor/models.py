from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.core.validators import RegexValidator
# Create your models here.

# Model used to detail what subjects a model is comfortable tutoring in
class Subject(models.Model):
    subject_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['subject_name']

    def __str__(self):
        return self.subject_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default="")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_addr = models.EmailField(max_length=200)
    #= for now, use simple text field for phone number, but later make sure we validate it somehow
    # use this? https://pypi.org/project/django-phone-field/
    pic = models.ImageField(upload_to='media/profile_picture', default = "default_profile_pic.png", blank=False)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True) # two places past decimal

    # List of subjects a User is able to offer tutoring services in
    subjects_can_help = models.ManyToManyField(Subject)

    # List of subjects User needs help with


    def __str__(self):
        return self.user.username
    def save(self):
        super().save()

SUBJECTS = [
    ('none', 'None'),
    ('african-american studies', 'African-American & African Studies'),
    ('anthropology', 'Anthropology'),
    ('astronomy', 'Astronomy'),
    ('biology', 'Biology'),
    ('chemistry', 'Chemistry'),
    ('economics', 'Economics'),
    ('french', 'French'),
    ('german', 'German'),
    ('physics', 'Physics'),
    ('mathematics', 'Mathematics'),
]

class Job(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    course = models.CharField(max_length=200, default="")
    subject = models.CharField(max_length=200, choices=SUBJECTS, default='None')
    notes = models.TextField(max_length=1000, default="")

    def __str__(self):
        return self.subject

def create_profile(sender, instance, created, **kwargs):
   if created:
        user_profile = Profile()
        user_profile.user = instance
        user_profile.first_name = user_profile.user.first_name
        user_profile.last_name = user_profile.user.last_name
        user_profile.email_addr = user_profile.user.email
        user_profile.save()

post_save.connect(create_profile, sender=User)
