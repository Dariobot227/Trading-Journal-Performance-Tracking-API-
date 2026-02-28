#automatic creation of profiles when a user is created, or once registerd
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):

    if created:
        Profile.objects.create(
            user=instance,
            Account_size=0,
            current_balance=0
        )