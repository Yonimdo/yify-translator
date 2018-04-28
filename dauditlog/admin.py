from django.contrib import admin

# Register your models here.
from dauditlog.models import Audit, Log, CheckingList


@admin.register(Log)
class LogManagement(admin.ModelAdmin):
    readonly_fields = ('user', 'request', 'request_body',
                       'response', 'uuid', 'error_message', 'func_name', 'passed', 'created', 'passed')
    list_display = ('uuid', 'func_name', 'created', 'passed', 'note')
    list_filter = ('func_name', 'created', 'passed')
    search_fields = ('uuid', 'func_name')


@admin.register(Audit)
class AuditManagement(admin.ModelAdmin):
    readonly_fields = ('log',
                       'log_uuid',
                       'func_name',
                       'request',
                       'response',
                       'error_message',
                       'created',
                       'passed',
                       )
    list_display = ('log_uuid', 'func_name', 'created', 'passed', 'note')
    list_filter = ('log_uuid', 'func_name', 'created', 'passed')
    search_fields = ('log_uuid', 'func_name')


admin.site.register(CheckingList)
