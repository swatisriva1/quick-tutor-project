from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    #first_name = models.CharField(max_length=200)
    #last_name = models.CharField(max_length=200)
    #email_addr = models.EmailField(max_length=200)
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    rating = models.DecimalField(max_digits=5, decimal_places=2) # two places past decimal
    # need a field for tutor or student -- radio buttons, but associated with
    # a field in the database...
    # also need one for ranking
