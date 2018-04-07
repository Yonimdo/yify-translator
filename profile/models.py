from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Todo: fields from the user.
    def __str__(self):
        return self.user.name
class UserFile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = models.FileField()
    def __str__(self):
        return self.file.name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
