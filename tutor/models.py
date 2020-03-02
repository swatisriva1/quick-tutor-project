from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    #first_name = models.CharField(max_length=200)
    #last_name = models.CharField(max_length=200)
    #email_addr = models.EmailField(max_length=200)
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_addr = models.EmailField(max_length=200)
    #= for now, use simple text field for phone number, but later make sure we validate it somehow
    # use this? https://pypi.org/project/django-phone-field/
    pic = models.ImageField(upload_to='profile_picture', default='/tutor/static/tutor/default_profile_pic.png', 
    blank=False)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True) # two places past decimal

    def __str__(self):
        return self.user.username
    def save(self):
        super().save()
        
#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

def create_profile(sender, instance, created, **kwargs):
   if created:
        user_profile = Profile()
        user_profile.user = instance
        user_profile.first_name = user_profile.user.first_name
        user_profile.last_name = user_profile.user.last_name
        user_profile.email_addr = user_profile.user.email
        user_profile.save()

post_save.connect(create_profile, sender=User)
