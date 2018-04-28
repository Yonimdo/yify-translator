from django.contrib import admin

from texts.models import LenguaText, OriginalText, Suggestion, SmartText


@admin.register(LenguaText)
class LogManagement(admin.ModelAdmin):
    list_display = ('uuid', 'values')
    list_filter = ('uuid', 'values')
    search_fields = ('uuid', 'values')


@admin.register(SmartText)
class AuditManagement(admin.ModelAdmin):
    readonly_fields = ('language', 'count')
    list_display = ('count', 'text', 'language')
    list_filter = ('count', 'text', 'language')
    search_fields = ('count', 'text', 'language')


@admin.register(OriginalText)
class AuditManagement(admin.ModelAdmin):
    readonly_fields = ('original', 'count')
    list_display = ('count', 'original')
    list_filter = ('count', 'original')
    search_fields = ('count', 'original')


@admin.register(Suggestion)
class AuditManagement(admin.ModelAdmin):
    readonly_fields = ('original','translation', 'count')
    list_display = ('original', 'translation', 'user_translation', 'from_language', 'to_language', 'count')
    list_filter = ('original', 'translation', 'user_translation', 'from_language', 'to_language', 'count')
    search_fields = ('original', 'translation', 'user_translation')

