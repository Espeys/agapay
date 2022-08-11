from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.SourceToken)
class SourceTokenAdmin(admin.ModelAdmin):

    date_hierarchy = 'created_at'

    list_display = [
        'action',
        'code',
        'created_by',
        'expired_at',
        'is_used',
        'state',
        'created_at',
        'updated_at',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
        'action',
        'expired_at',
        'is_used',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'action',
        'code',
        'created_by__username',
        'is_used',
    ]