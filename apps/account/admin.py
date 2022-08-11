from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import (
    forms,
    models,
)


class ProfileFollowerInline(admin.TabularInline):
    model = models.Profile.followers.through
    fk_name = 'follower'
    form = forms.ProfileFollowerForm

class ProfileFollowingInline(admin.TabularInline):
    model = models.Profile.followers.through
    fk_name = 'following'
    form = forms.ProfileFollowerForm


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User', {
            'classes': ('wide',),
            'fields': (
                'user',
                'photo',
                'anonymous',
                'icon_name',
                'icon_color',
                'fullname',
                'about',
                'location',
                'tel_no',
                'mobile_no',
                'birthdate',
                'office_start_time',
                'office_end_time' ,
                'website',
                'bookmarks',
                'is_verified',
                'is_certified',
                'is_anonymous',
                'state',
                'created_at',
                'updated_at',
            ),
        }),
    ]

    list_display = [
        'slug',
        'user',
        'created_at',
        'updated_at',
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
        'user__username',
        'user__email',
        'fullname',
        'description',
        'slug'
    ]

    inlines = (
        ProfileFollowerInline,
        ProfileFollowingInline
    )

    filter_horizontal = ('bookmarks',)


@admin.register(models.ProfileFollower)
class ProfileFollowerAdmin(admin.ModelAdmin):
    list_display = [
        'slug',
        'follower',
        'following',
        'created_at',
        'updated_at',
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
        'slug'
        'follower__slug',
        'following__slug',
        'follower__user__email',
        'following__user__email',
        'follower__user__username',
        'following__user__username',
    ]

admin.site.register(models.ProfileConnection)

# admin.site.register(models.MoodTrack)

admin.site.register(models.ProfileReport)

admin.site.register(models.Support)

admin.site.register(models.ChatRoom)

admin.site.register(models.Message)

admin.site.register(models.Notification)

admin.site.register(models.Activity)