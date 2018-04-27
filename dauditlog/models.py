import uuid as uid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.functions import Now


class Log(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    request = models.TextField(blank=False, null=False)
    request_body = models.TextField(blank=False, null=False)
    response = models.TextField(null=True, blank=True)
    uuid = models.UUIDField(auto_created=True, default=uid.uuid4)
    error_message = models.TextField(null=True, blank=True)
    created = models.TimeField(auto_created=True, default=Now)
    passed = models.BooleanField(null=False, default=False)
    note = models.TextField(null=True, blank=True)

    # Todo: fields from the user.
    def __str__(self):
        return "{} - {}".format(self.uuid, self.request)


# Create your models here.
class Audit(models.Model):
    # Todo: fields from the user.
    log = models.ForeignKey(Log, null=True, blank=True, on_delete=models.CASCADE)
    func_name = models.TextField(blank=False, null=False)
    request = models.TextField(blank=False, null=False)
    response = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    created = models.TimeField(auto_created=True, default=Now)
    passed = models.BooleanField(blank=False, null=False, default=False)
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.log.uuid, self.func_name)
