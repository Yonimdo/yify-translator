from django.contrib import admin

from texts.models import LenguaText, OriginalText, Suggestion

admin.site.register(LenguaText)
admin.site.register(OriginalText)
admin.site.register(Suggestion)
