from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.core.validators import RegexValidator
from django_google_maps import fields as map_fields


# Create your models here.

# Model used to detail what subjects a model is comfortable tutoring in
class Subject(models.Model):
    subject_name = models.CharField(max_length=30)

    class Meta:
        ordering = ['subject_name']

    def __str__(self):
        return self.subject_name


class Profile(models.Model):

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, default="")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, default='+999999999')
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    first_name = models.CharField(max_length=200, default='First')
    last_name = models.CharField(max_length=20, default='Last')
    email_addr = models.EmailField(max_length=200, default='example@email.com')
    #= for now, use simple text field for phone number, but later make sure we validate it somehow
    # use this? https://pypi.org/project/django-phone-field/
    pic = models.ImageField(upload_to='profile_picture', default='/tutor/static/tutor/default_profile_pic.png',
                            blank=False)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # two places past decimal

    # List of subjects a User is able to offer tutoring services in
    subjects_can_help = models.ManyToManyField(Subject)

    # List of subjects User needs help with


    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



SUBJECTS = [
    ('None', 'None'),
    ('African-american studies', 'African-American & African Studies'),
    ('Anthropology', 'Anthropology'),
    ('Astronomy', 'Astronomy'),
    ('Biology', 'Biology'),
    ('Chemistry', 'Chemistry'),
    ('Economics', 'Economics'),
    ('French', 'French'),
    ('German', 'German'),
    ('Physics', 'Physics'),
    ('Mathematics', 'Mathematics'),
]
LOCATIONS = [
    ("Alderman Library", "Alderman Library"),
    ("Aquatic and Fitness Center", "Aquatic and Fitness Center"),
    ("Astronomy Building", "Astronomy Building"),
    ("Birdwood Golf Course", "Birdwood Golf Course"),
    ("Bayly Building", "Bayly Building"),
    ("Brooks Hall (first floor and basement only)", "Brooks Hall (first floor and basement only)"),
    ("Bryan Hall", "Bryan Hall"),
    ("Brown College Library", "Brown College Library"),
    ("Bryant Hall", "Bryant Hall"),
    ("New Cabell Hall", "New Cabell Hall"),
    ("Campbell Hall", "Campbell Hall"),
    ("Cauthen House", "Cauthen House"),
    ("Chemical Engineering Building", "Chemical Engineering Building"),
    ("Claude Moore Nursing", "Claude Moore Nursing"),
    ('Cobb Hall', 'Cobb Hall'),
    ("Cocke Hall", "Cocke Hall"),
     ("Chemistry Building (key needed for elevator)", "Chemistry Building (key needed for elevator)"),
     ("Clark Hall", "Clark Hall"),
     ("Clemons Library", "Clemons Library"),
     ("Dell 1", "Dell 1"),
     ('Dell 2', "Dell 2"),
     ('Dawsons Row Residence 1', 'Dawsons Row Residence 1'),
     ('Drama Education Building (key needed for elevator)', 'Drama Education Building (key needed for elevator)'),
     ('Hospital West, Davis Wing', 'Hospital West, Davis Wing'),
     ('Fayerweather Hall', 'Fayerweather Hall'),
     ('French House', 'French House'),
     ('Gibson Hall', 'Gibson Hall'),
      ('Gilmer Hall', 'Gilmer Hall'),
      ('Darden School', 'Darden School'),
      ('Halsey Hall', 'Halsey Hall'),
      ('Hotel D, East Range', 'Hotel D,East Range'),
      ('Jordan Hall', 'Jordan Hall'),
      ('Kerchof Hall (first floor only)', 'Kerchof Hall'),
      ('Levering Hall', 'Levering Hall'),
      ('Lambeth House', 'Lambeth House'),
      ('Lower West Oval Room, Rotunda', 'Lower West Oval Room, Rotunda'),
      ('McLeod Hall', 'McLeod Hall'),
      ('Mechanical Engineering Building', 'Mechanical Engineering Building'),
      ('Old Medical School', 'Old Medical School'),
      ('Memorial Gymnasium', 'Memorial Gymnasium'),
      ('Multistory Building (Old Hospital)', 'Multistory Building (Old Hospital)'),
      ('Monroe Hill Range', 'Monroe Hill Range'),
      ('Minor Hall', 'Minor Hall'),
      ('Monroe Hall', 'Monroe Hall'),
      ('Maury Hall', 'Maury Hall)'),
       ('Materials Science Building', 'Materials Science Building'),
       ('Nau Hall', 'Nau Hall'),
       ('Newcomb Hall', 'Newcomb Hall'),
       ('McCormick Observatory', 'McCormick Observatory'),
       ('Old Cabell Hall', 'Old Cabell Hall'),
       ('Olsson Hall', 'Olsson Hall'),
       ('Peabody Hall', "Peabody Hall"),
       ('Physics Building', 'Physics Building'),
       ('Pavilion V (no ADA access)', 'Pavilion V (no ADA access)'),
       ('Pavilion VIII (no ADA access)', 'Pavilion VIII (no ADA access)'),
       ('(Randall Hall (first floor only)', '(Randall Hall (first floor only)'),
       ('National Radio Astronomy Observatory (first floor only)',
        'National Radio Astronomy Observatory (first floor only)'),
       ('Robertson Hall', 'Robertson Hall'),
       ('Slaughter Recreation Center', 'Slaughter Recreation Center'),
       ('Ruffner Hall', 'Ruffner Hall'),
       ('Rice Hall', 'Rice Hall'),
       ('Rouss Hall', 'Rouss Hall'),
       ('Rotunda', 'Rotunda'),
       ('Ruffin Hall', 'Ruffin Hall'),
       ('Shea House', 'Shea House'),
       ('Shannon House', 'Shannon House'),
       ('Slaughter Hall', 'Slaughter Hall'),
       ('Barracks Stables', 'Barracks Stables'),
       ('Stacey Hall', "Stacey Hall"),
       ('Thornton Hall (D Wing, O Level not accessible)', 'Thornton Hall'),
       ('Wilson Hall', 'Wilson Hall')
]


class Job(models.Model):
    customer_user = models.ForeignKey(User, related_name='Customer', on_delete=models.CASCADE, null=True, blank=True) #customer user
    tutor_user = models.ForeignKey(User, related_name='Tutor', on_delete=models.CASCADE, null=True, blank=True) #tutor user
    customer_profile = models.ForeignKey('Profile', related_name='CustomerProfile', on_delete=models.CASCADE, null=True, blank=True)
    tutor_profile = models.ForeignKey('Profile', related_name='TutorProfile', on_delete=models.CASCADE, null=True, blank=True)
    course = models.CharField(max_length=200, default="")
    subject = models.CharField(max_length=200, choices=SUBJECTS, default=SUBJECTS[0][0])
    notes = models.TextField(max_length=1000, default="")
    location = models.CharField(max_length=200, choices=LOCATIONS, default='None')
    isConfirmed = models.BooleanField(default=True)

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
#post_save.connect(create_job, sender=User)
