from django.contrib import admin

# Register your models here.
from dauditlog.models import Audit, Log

admin.site.register(Log)
admin.site.register(Audit)
