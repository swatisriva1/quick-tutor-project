from django.db import models

# Create your models here.

class Profile(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_addr = models.EmailField(max_length=200)
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    rating = models.DecimalField(max_digits=5, decimal_places=2) # two places past decimal
    # need a field for tutor or student -- radio buttons, but associated with
    # a field in the database...
    # also need one for ranking
