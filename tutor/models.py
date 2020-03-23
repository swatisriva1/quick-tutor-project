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
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    # don't want to use simple text field for phone number
    # (want to validate) but not sure what to use
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_addr = models.EmailField(max_length=200)
    # = for now, use simple text field for phone number, but later make sure we validate it somehow
    # use this? https://pypi.org/project/django-phone-field/
    pic = models.ImageField(upload_to='profile_picture', default='/tutor/static/tutor/default_profile_pic.png',
                            blank=False)
    rating = models.DecimalField(max_digits=5, decimal_places=2, null=True)  # two places past decimal

    # List of subjects a User is able to offer tutoring services in
    subjects_can_help = models.ManyToManyField(Subject)

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
LOCATIONS = [
    "Alderman Library",
    "Aquatic and Fitness Center",
    "Astronomy Building",
    "Birdwood Golf Course",
    "Bayly Building (staff assistance required to use freight elevator)",
    "Brooks Hall (first floor and basement only)",
    "Bryan Hall",
    "Brown College Library",
    "Bryant Hall",
    "New Cabell Hal",
    "Campbell Hall",
    "Cauthen House",
    "Chemical Engineering Building",
    "Claude Moore Nursing",
    'Cobb Hall',
    "Cocke Hall",
    "Chemistry Building (key needed for elevator)",
    "Clark Hall",
    "Clemons Library",
    "Dell 1",
    'Dell 2',
    'Dawsons Row Residence 1',
    'Drama Education Building (key needed for elevator)',
    'Hospital West, Davis Wing',
    'Fayerweather Hall',
    'French House',
    'Gibson Hall',
    'Gilmer Hall (key needed for elevator)',
    'Darden School',
    'Halsey Hall (entering from the Clark Hall side there are no limitations)',
    'Hotel D, East Range',
    'Home of the Instructor',
    'Charlottesville Ice Park',
    'International Study program outside the U.S.',
    'Judge Advocate General School',
    'Jordan Hall (accessible entrances locked at night)',
    'Kerchof Hall (first floor only)',
    'Levering Hall (first floor only)',
    'Lambeth House',
    'Luther P. Jackson House (first floor only)',
    'Lower West Oval Room, Rotunda',
    'McLeod Hall',
    'Mechanical Engineering Building',
    'Old Medical School',
    'Memorial Gymnasium (first floor and basement only; assistance needed at locked entrances; no access across the track on the second floor)',
    'Multistory Building (Old Hospital)',
    'Monroe Hill Range',
    'Minor Hall',
    'Monroe Hall',
    'Maury Hall (no ADA access to the basement; access to first and second floors through separate doors)',
    'Materials Science Building',
    'Mary Munford House',
    'Nau Hall',
    'Newcomb Hall',
    'No Room Needed',
    'UVA/VT Center in Falls Church',
    'McCormick Observatory',
    'Old Cabell Hall',
    'Olsson Hall',
    'Peabody Hall',
    'Physics Building (assistance may be needed for freight elevator)',
    'Pavilion V (no ADA access)',
    'Pavilion VIII (no ADA access)',
    'Randall Hall (first floor only)',
    'National Radio Astronomy Observatory (first floor only)',
    'Robertson Hall',
    'Nuclear Reactor',
    'Slaughter Recreation Center',
    'Ruffner Hall',
    'Rice Hall',
    'Rouss Hall',
    'Rotunda',
    'Ruffin Hall',
    'Shea House',
    'Shannon House',
    'Slaughter Hall',
    'Barracks Stables',
    'Stacey Hall',
    'Thornton Hall (D Wing, O Level not accessible)',
    'Wilson Hall',
    'Wintergreen Resort',
    'Withers-Brown Hall',
    'Zehmer Hall Annex',
    'Zehmer Hall',

]


class Job(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey('Profile', on_delete=models.CASCADE, null=True, blank=True)
    course = models.CharField(max_length=200, default="")
    subject = models.CharField(max_length=200, choices=SUBJECTS, default='None')
    notes = models.TextField(max_length=1000, default="")
    location = models.CharField(max_length=200, choices=LOCATIONS, default='None')

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
