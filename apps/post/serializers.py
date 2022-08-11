from apps.account.serializers import (
  Userv2Serializer,
  UserWithProfileSerializer,
  AnonymousUserSerializer,
  ChatRoomSerializer as AccountChatRoomSerializer
)
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.account.models import Support, Profile
from . import models

from base import utils as base_utils

import json

User = get_user_model()


class PostItemSerializer(serializers.Serializer):

    slug = serializers.CharField()
    shared_post = serializers.SerializerMethodField()
    banner = serializers.SerializerMethodField()
    name = serializers.CharField()
    title = serializers.CharField()
    description = serializers.CharField()
    location = serializers.CharField()
    weblink = serializers.URLField()
    tel_no = serializers.CharField()
    mobile_no = serializers.CharField()
    sched_start = serializers.DateTimeField()
    sched_end = serializers.DateTimeField()
    visibility_type = serializers.CharField()
    item_type = serializers.CharField()
    promotion_type = serializers.CharField()
    censorship = serializers.BooleanField()

    is_anonymous = serializers.BooleanField()
    is_verified = serializers.BooleanField()

    geo_lat = serializers.FloatField()
    geo_long = serializers.FloatField()
    geo_full_address = serializers.CharField()

    miles = serializers.FloatField()
    mood_type = serializers.CharField()
    help_type = serializers.CharField()

    is_liked = serializers.SerializerMethodField()
    is_shared = serializers.SerializerMethodField()
    is_saved = serializers.SerializerMethodField()

    like_count = serializers.SerializerMethodField()
    share_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()

    tags = serializers.SerializerMethodField()

    created_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()

    def get_shared_post(self, obj):
        if obj.shared_post:
            coord = (obj.shared_post.geo_lat, obj.shared_post.geo_long)
            obj.shared_post.miles = base_utils.get_distance(
                base_utils.get_lat_long(obj.request), coord
            )
            obj.shared_post.request = obj.request
            return PostItemSerializer(obj.shared_post).data
        return None

    def get_banner(self, obj):
        return obj.get_banner

    def get_tags(self, obj):
        # return PostTagSerializer(obj.tags, many=True).data
        return list(obj.tags.values_list('text', flat=True))

    def get_created_by(self, obj):
        if obj.is_anonymous:
            return AnonymousUserSerializer(obj.created_by).data

        if obj.created_by:
            return UserSerializer(obj.created_by).data

    def get_is_liked(self, obj):
        return obj.likes.filter(slug=obj.request).exists()

    def get_is_saved(self, obj):
        try:
            return Profile.people.get(slug=obj.request
            ).bookmarks.filter(slug=obj.slug).exists()
        except: return False

    def get_is_shared(self, obj):
        return models.PostItem.objects.state_active().filter(
                shared_post__slug=obj.slug,
                created_by__slug=obj.request
            ).exists()

    def get_like_count(self, obj):
        return obj.like_count

    def get_share_count(self, obj):
        return obj.share_count

    def get_comment_count(self, obj):
        return obj.comment_count


class PostHistorySerializer(serializers.Serializer):
    action = serializers.CharField()
    from_attrs = serializers.JSONField()
    to_attrs = serializers.JSONField()
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        try:
            if obj.created_by:
                return UserSerializer(obj.created_by).data
        except:
            return None


class PostReportSerializer(serializers.Serializer):
    slug = serializers.CharField()
    post = serializers.SerializerMethodField()
    reason = serializers.CharField()
    description = serializers.CharField()
    reported_by = serializers.SerializerMethodField()

    def get_post(self, obj):
        if obj.post:
            return obj.post.slug
        return None

    def get_reported_by(self, obj):
        if obj.reported_by:
            return obj.reported_by.slug
        return None


class UserSerializer(Userv2Serializer):
    pass


class MoodSerializer(serializers.Serializer):
    slug = serializers.CharField()
    mood = serializers.CharField()
    description = serializers.CharField()
    updated_at = serializers.DateTimeField()


class CommentSerializer(serializers.Serializer):
    slug = serializers.CharField()
    description = serializers.CharField()
    is_anonymous = serializers.BooleanField()
    # replies
    children = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField()
    created_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.is_anonymous:
            return AnonymousUserSerializer(obj.created_by).data

        if obj.created_by:
            return UserSerializer(obj.created_by).data

    def get_children(self, obj):
        return CommentSerializer(obj.children.filter(
                state=obj.STATE_ACTIVE
            ), many=True).data

class PostTagSerializer(serializers.Serializer):
    slug = serializers.CharField()
    text = serializers.CharField()


class DiaryAggregateSerializer(serializers.Serializer):
    weight = serializers.FloatField()
    mood = serializers.CharField()


class PostSupportSerializer(serializers.Serializer):
    slug = serializers.CharField()
    type = serializers.CharField()
    attrs = serializers.SerializerMethodField()
    reason = serializers.CharField()
    description = serializers.CharField()
    status = serializers.CharField()


    def get_attrs(self, obj):
        if obj.type == Support.TYPE_POST:

            try:
                post = models.PostItem.objects.state_active().get(
                        slug=json.loads(obj.attrs_json).get('post_slug', None)
                    )
                post.miles = base_utils.get_distance(
                    base_utils.get_lat_long(obj.ip),
                    (post.geo_lat, post.geo_long)
                )
                post.request = obj.request
                return PostItemSerializer(post).data
            except Exception as e: raise Exception(e)
        return None

class ChatRoomSerializer(AccountChatRoomSerializer):
    pass