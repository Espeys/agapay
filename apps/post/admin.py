from django.contrib import admin

from . import models


@admin.register(models.PostItem)
class PostItemAdmin(admin.ModelAdmin):

    list_display = [
        'slug',
        'description',
        'created_by',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'description',
        'slug'
    ]


@admin.register(models.PostReport)
class PostReportAdmin(admin.ModelAdmin):

    list_display = [
        'slug',
        'post',
        'reported_by',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'reason',
        'description',
        'slug'
    ]



@admin.register(models.PostAuditTrail)
class PostAuditTrailAdmin(admin.ModelAdmin):

    list_display = [
        'slug',
        'post',
        'created_by',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'slug',
        'description',
    ]



admin.site.register(models.PostTag)


@admin.register(models.PostComment)
class PostCommentAdmin(admin.ModelAdmin):

    list_display = [
        'slug',
        'description',
        'created_by',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'description',
        'slug'
    ]



@admin.register(models.PostCommentReport)
class PostCommentReportAdmin(admin.ModelAdmin):

    list_display = [
        'slug',
        'comment',
        'reported_by',
    ]

    list_filter = [
        'state',
        'created_at',
        'updated_at',
    ]

    readonly_fields = [
        'slug',
        'created_at',
        'updated_at',
    ]

    search_fields = [
        'reason',
        'description',
        'slug'
    ]


