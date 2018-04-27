from django.contrib import admin

# Register your models here.
from dauditlog.models import Audit, Log,CheckingList

admin.site.register(Log)
admin.site.register(Audit)
admin.site.register(CheckingList)
