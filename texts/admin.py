from django.contrib import admin

from texts.models import LenguaText, OriginalText, Suggestion, SmartText


@admin.register(LenguaText)
class LenguaTextManagement(admin.ModelAdmin):
    list_display = ('uuid', 'values')
    search_fields = ('uuid', 'values')


@admin.register(SmartText)
class SmartTextManagement(admin.ModelAdmin):
    readonly_fields = ('language', 'text_origin', 'count')
    list_display = ('count', 'text', 'language')
    search_fields = ('count', 'text', 'language')


@admin.register(OriginalText)
class OriginalTextManagement(admin.ModelAdmin):
    readonly_fields = ('original', 'text', 'count')
    list_display = ('count', 'original')
    search_fields = ('count', 'original')


@admin.register(Suggestion)
class SuggestionManagement(admin.ModelAdmin):
    readonly_fields = ('original', 'translation', 'count')
    list_display = ('original', 'translation', 'user_translation', 'from_language', 'to_language', 'count')
    list_filter = ('original', 'translation', 'user_translation', 'from_language', 'to_language', 'count')
    search_fields = ('original', 'translation', 'user_translation')
