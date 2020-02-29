from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_addr = models.EmailField(max_length=200)
    #= for now, use simple text field for phone number, but later make sure we validate it somehow
    # use this? https://pypi.org/project/django-phone-field/
    phone_num = models.CharField(default="", max_length=10)
    rating = models.DecimalField(max_digits=5, decimal_places=2) # two places past decimal
