from django.contrib import admin

from texts.models import LenguaText, OriginalText, Suggestion, SmartText

admin.site.register(LenguaText)
admin.site.register(SmartText)
admin.site.register(OriginalText)
admin.site.register(Suggestion)
