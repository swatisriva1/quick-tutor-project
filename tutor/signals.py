from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
# from utilities.utils import get_filename, rotate_image


@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()

# @receiver(post_save, sender=Profile)
# def create_profile(sender, instance, **kwargs):
#     User.Profile.objects.get_or_create(user=instance)

# @receiver(post_save, sender=Profile)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

# For rotating profile picture to correct orientation
# Taken from https://medium.com/@giovanni_cortes/rotate-image-in-django-when-saved-in-a-model-8fd98aac8f2a
""" @receiver(post_save, sender=Profile, dispatch_uid="update_image_profile")
def update_image(sender, instance, **kwargs):
  if instance.image:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fullpath = BASE_DIR + instance.image.url
    rotate_image(fullpath) """

# From Corey Schafer tutorial, in case we realize above is incorrect for signals
# https://www.youtube.com/watch?v=FdVuKt_iuSI
'''@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() '''   
    

