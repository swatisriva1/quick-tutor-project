from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django import forms
from django.core.validators import RegexValidator
from django_google_maps import fields as map_fields    
from PIL import Image, ExifTags


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
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, help_text="Phone number must be entered in the format: '9999999999'. Up to 15 digits allowed.")
    first_name = models.CharField(max_length=30, default='First')
    last_name = models.CharField(max_length=30, default='Last')
    email_addr = models.EmailField(max_length=200, default='example@email.com', help_text="Ex: example@email.com")
    pic = models.ImageField(upload_to='profile_picture', default = "default_profile_pic.png", blank=True, help_text = "Uploading a profile picture makes it easier for your tutor/student to recognize you.")
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, default=5.0) # two places past decimal
    # List of subjects a User is able to offer tutoring services in
    subjects_can_help = models.ManyToManyField(Subject, help_text="Crtl-click to select multiple subjects; select 'None' if you do not wish to tutor")
    started = models.BooleanField(default=False)
    jobinteractions = models.IntegerField(blank=True, default=1)
    # Method that returns profile pic to be displayed (default or user-uploaded)
    @property
    def get_pic_url(self):
        if self.pic and hasattr(self.pic, 'url'):
            return self.pic.url
        else:
            # return "/media/default_profile_pic.png"
            return "/static/tutor/default_profile_pic.png"

    # Method to rotate profile picture into correct orientation
    # Taken from https://medium.com/@giovanni_cortes/rotate-image-in-django-when-saved-in-a-model-8fd98aac8f2a
    """ def rotate_image(filepath):
        try:
            image = Image.open(filepath)
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = dict(image._getexif().items())

            if exif[orientation] == 3:
                image = image.rotate(180, expand=True)
            elif exif[orientation] == 6:
                image = image.rotate(270, expand=True)
            elif exif[orientation] == 8:
                image = image.rotate(90, expand=True)
            image.save(filepath)
            image.close()
        except (AttributeError, KeyError, IndexError):
            # cases: image don't have getexif
            pass """

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



SUBJECTS = [
    ('None', 'None'),
    ('African-American studies', 'African-American & African Studies'),
    ('Anthropology', 'Anthropology'),
    ('Astronomy', 'Astronomy'),
    ('Biology', 'Biology'),
    ('Chemistry', 'Chemistry'),
    ('Computer Science','Computer Science'),
    ('Economics', 'Economics'),
    ('French', 'French'),
    ('German', 'German'),
    ('Physics', 'Physics'),
    ('Mathematics', 'Mathematics'),
]
LOCATIONS = [
    ("Alderman Library in Charlottesville, Virginia", "Alderman Library"),
    ("Aquatic and Fitness Center in Charlottesville, Virginia", "Aquatic and Fitness Center"),
    ("Astronomy Building in Charlottesville, Virginia", "Astronomy Building"),
    ("Birdwood Golf Course in Charlottesville, Virginia", "Birdwood Golf Course"),
    ("Bayly Building in Charlottesville, Virginia", "Bayly Building"),
    ("Brooks Hall in Charlottesville, Virginia", "Brooks Hall (first floor and basement only)"),
    ("Bryan Hall in Charlottesville, Virginia", "Bryan Hall"),
    ("Brown College Library in Charlottesville, Virginia", "Brown College Library"),
    ("Bryant Hall in Charlottesville, Virginia", "Bryant Hall"),
    ("New Cabell Hall", "New Cabell Hall"),
    ("Campbell Hall in Charlottesville, Virginia", "Campbell Hall"),
    ("Cauthen House in Charlottesville, Virginia", "Cauthen House"),
    ("Chemical Engineering Building in Charlottesville, Virginia", "Chemical Engineering Building"),
    ("Claude Moore Nursing in Charlottesville, Virginia", "Claude Moore Nursing"),
    ('Cobb Hall in Charlottesville, Virginia', 'Cobb Hall'),
    ("Cocke Hall", "Cocke Hall"),
     ("Chemistry Building in Charlottesville, Virginia", "Chemistry Building (key needed for elevator)"),
     ("Clark Hall in Charlottesville, Virginia", "Clark Hall"),
     ("Clemons Library in Charlottesville, Virginia", "Clemons Library"),
     ("Dell 1 in Charlottesville, Virginia", "Dell 1"),
     ('Dell 2 in Charlottesville, Virginia', "Dell 2"),
     ('Dawsons Row Residence 1 in Charlottesville, Virginia', 'Dawsons Row Residence 1'),
     ('Drama Education Building in Charlottesville, Virginia', 'Drama Education Building (key needed for elevator)'),
     ('Hospital West, Davis Wing in Charlottesville, Virginia', 'Hospital West, Davis Wing'),
     ('Fayerweather Hall in Charlottesville, Virginia', 'Fayerweather Hall'),
     ('French House in Charlottesville, Virginia', 'French House'),
     ('Gibson Hall in Charlottesville, Virginia', 'Gibson Hall'),
      ('Gilmer Hall in Charlottesville, Virginia', 'Gilmer Hall'),
      ('Darden School in Charlottesville, Virginia', 'Darden School'),
      ('Halsey Hall in Charlottesville, Virginia', 'Halsey Hall'),
      ('Hotel D, East Range in Charlottesville, Virginia', 'Hotel D,East Range'),
      ('Jordan Hall in Charlottesville, Virginia', 'Jordan Hall'),
      ('Kerchof Hall in Charlottesville, Virginia', 'Kerchof Hall'),
      ('Levering Hall in Charlottesville, Virginia', 'Levering Hall'),
      ('Lambeth House in Charlottesville, Virginia', 'Lambeth House'),
      ('McLeod Hall in Charlottesville, Virginia', 'McLeod Hall'),
      ('Mechanical Engineering Building in Charlottesville, Virginia', 'Mechanical Engineering Building'),
      ('Old Medical School in Charlottesville, Virginia', 'Old Medical School'),
      ('Memorial Gymnasium in Charlottesville, Virginia', 'Memorial Gymnasium'),
      ('Multistory Building in Charlottesville, Virginia', 'Multistory Building (Old Hospital)'),
      ('Monroe Hill Range in Charlottesville, Virginia', 'Monroe Hill Range'),
      ('Minor Hall in Charlottesville, Virginia', 'Minor Hall'),
      ('Monroe Hall in Charlottesville, Virginia', 'Monroe Hall'),
      ('Maury Hall in Charlottesville, Virginia', 'Maury Hall)'),
       ('Materials Science Building in Charlottesville, Virginia', 'Materials Science Building'),
       ('Nau Hall in Charlottesville, Virginia', 'Nau Hall'),
       ('Newcomb Hall in Charlottesville, Virginia', 'Newcomb Hall'),
       ('McCormick Observatory in Charlottesville, Virginia', 'McCormick Observatory'),
       ('Old Cabell Hall in Charlottesville, Virginia', 'Old Cabell Hall'),
       ('Olsson Hall in Charlottesville, Virginia', 'Olsson Hall'),
       ('Peabody Hall in Charlottesville, Virginia', "Peabody Hall"),
       ('Physics Building in Charlottesville, Virginia', 'Physics Building'),
       ('Pavilion V in Charlottesville, Virginia', 'Pavilion V (no ADA access)'),
       ('Pavilion VIII in Charlottesville, Virginia', 'Pavilion VIII (no ADA access)'),
       ('(Randall Hall in Charlottesville, Virginia', '(Randall Hall (first floor only)'),
       ('National Radio Astronomy Observatory in Charlottesville, Virginia',
        'National Radio Astronomy Observatory (first floor only)'),
       ('Robertson Hall in Charlottesville, Virginia', 'Robertson Hall'),
    ('Rotunda Charlottesville, Virginia', 'Rotunda'),
       ('Slaughter Recreation Center in Charlottesville, Virginia', 'Slaughter Recreation Center'),
       ('Ruffner Hall in Charlottesville, Virginia', 'Ruffner Hall'),
       ('Rice Hall in Charlottesville, Virginia', 'Rice Hall'),
       ('Rouss Hall in Charlottesville, Virginia', 'Rouss Hall'),
       ('Ruffin Hall in Charlottesville, Virginia', 'Ruffin Hall'),
       ('Shea House in Charlottesville, Virginia', 'Shea House'),
       ('Shannon House in Charlottesville, Virginia', 'Shannon House'),
       ('Slaughter Hall in Charlottesville, Virginia', 'Slaughter Hall'),
       ('Barracks Stables in Charlottesville, Virginia', 'Barracks Stables'),
       ('Stacey Hall in Charlottesville, Virginia', "Stacey Hall"),
       ('Thornton Hall in Charlottesville, Virginia', 'Thornton Hall'),
       ('Wilson Hall in Charlottesville, Virginia', 'Wilson Hall')
]


class Job(models.Model):
    customer_user = models.ForeignKey(User, related_name='Customer', on_delete=models.CASCADE, null=True, blank=True) #customer user
    tutor_user = models.ForeignKey(User, related_name='Tutor', on_delete=models.CASCADE, null=True, blank=True) #tutor user
    customer_profile = models.ForeignKey('Profile', related_name='CustomerProfile', on_delete=models.CASCADE, null=True, blank=True)
    tutor_profile = models.ForeignKey('Profile', related_name='TutorProfile', on_delete=models.CASCADE, null=True, blank=True)
    course_validator = RegexValidator(regex=r'[A-Z]{2,4} \d{4}', message="Enter a valid course code using following format: TEST 2010 (Make sure to capitalize the course subject!)")
    course = models.CharField(validators=[course_validator], max_length=9, default="", help_text="Ex: ECON 2010, MATH 1010")
    subject = models.CharField(max_length=200, choices=SUBJECTS, help_text="Select a subject that you need help in.", default=SUBJECTS[0][0])
    notes = models.TextField(max_length=250, default="", help_text="Any additional notes you might have about your request?", blank=True)
    location = models.CharField(max_length=200, choices=LOCATIONS, help_text="Select a meeting spot for your session.", default='None')
    session_date = models.DateTimeField(auto_now=True)
    isConfirmed = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    isComplete = models.BooleanField(default=False)
    last_tutored_by = models.ForeignKey(User, related_name='lastTutor', on_delete=models.CASCADE, null=True, blank=True) #last previous tutor
    isCanceled = models.BooleanField(default=False)


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
