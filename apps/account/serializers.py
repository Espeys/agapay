from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers


from .models import Profile

User = get_user_model()


class AnonymousUserSerializer(serializers.Serializer):
    slug = serializers.CharField()
    icon_name = serializers.SerializerMethodField()
    icon_color = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    is_anonymous = serializers.SerializerMethodField()
    is_dark_mode = serializers.SerializerMethodField()


    def get_full_name(self, obj):
        return obj.anonymous

    def get_icon_name(self, obj):
        return obj.icon_name

    def get_icon_color(self, obj):
        return obj.icon_color

    def get_is_anonymous(self, obj):
        return obj.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.is_dark_mode



class UserSerializer(serializers.Serializer):
    slug =serializers.SerializerMethodField()
    username = serializers.CharField()
    full_name = serializers.SerializerMethodField()
    icon_name = serializers.SerializerMethodField()
    icon_color = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    is_certified = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()
    # permissions = serializers.SerializerMethodField()
    is_anonymous = serializers.SerializerMethodField()
    is_dark_mode = serializers.SerializerMethodField()

    def get_permissions(self, obj):
        return obj.profile.permissions

    def get_groups(self, obj):
        return obj.profile.groups

    def get_photo(self, obj):
        return obj.profile.get_photo

    def get_full_name(self, obj):
        return obj.profile.fullname

    def get_is_verified(self, obj):
        return obj.profile.is_verified

    def get_is_certified(self, obj):
        return obj.profile.is_certified

    def get_slug(self, obj):
        return obj.profile.slug

    def get_icon_name(self, obj):
        return obj.profile.icon_name

    def get_icon_color(self, obj):
        return obj.profile.icon_color

    def get_is_anonymous(self, obj):
        return obj.profile.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.profile.is_dark_mode


class ProfileSerializer(serializers.Serializer):
    email = serializers.EmailField()
    about = serializers.CharField()
    bio = serializers.CharField()
    location = serializers.CharField()
    tel_no = serializers.CharField()
    mobile_no = serializers.CharField()
    website = serializers.URLField()
    service_type = serializers.CharField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    connection_count = serializers.SerializerMethodField()
    emergency_contact_person = serializers.CharField()
    emergency_contact_number = serializers.CharField()

    # connections

    tags = serializers.SerializerMethodField()

    def get_follower_count(self, obj):
        return obj.follower_count

    def get_following_count(self, obj):
        return obj.following_count

    def get_connection_count(self, obj):
        return obj.connection_count

    def get_tags(self, obj):
        # return ProfileTagSerializer(obj.tags, many=True).data
        return list(obj.tags.values_list('text', flat=True))


class ProfileTagSerializer(serializers.Serializer):
    slug = serializers.CharField()
    text = serializers.CharField()


class FollowerSerializer(serializers.Serializer):
    slug =serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    icon_name = serializers.SerializerMethodField()
    icon_color = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    is_certified = serializers.SerializerMethodField()
    is_anonymous = serializers.SerializerMethodField()
    is_dark_mode = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    # more details maybe

    def get_slug(self, obj):
        return obj.follower.slug

    def get_username(self, obj):
        return obj.follower.user.username

    def get_full_name(self, obj):
        return obj.follower.fullname

    def get_photo(self, obj):
        return obj.follower.get_photo

    def get_icon_name(self, obj):
        return obj.follower.icon_name

    def get_icon_color(self, obj):
        return obj.follower.icon_color

    def get_is_anonymous(self, obj):
        return obj.follower.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.follower.is_dark_mode


    def get_is_verified(self, obj):
        return obj.follower.is_verified

    def get_is_certified(self, obj):
        return obj.follower.is_certified

    def get_groups(self, obj):
        return obj.follower.groups




class FollowingSerializer(FollowerSerializer):

    def get_slug(self, obj):
        return obj.following.slug

    def get_username(self, obj):
        return obj.following.user.username

    def get_full_name(self, obj):
        return obj.following.fullname

    def get_photo(self, obj):
        return obj.following.get_photo

    def get_icon_name(self, obj):
        return obj.following.icon_name

    def get_icon_color(self, obj):
        return obj.following.icon_color

    def get_is_anonymous(self, obj):
        return obj.following.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.following.is_dark_mode

    def get_is_verified(self, obj):
        return obj.following.is_verified

    def get_is_certified(self, obj):
        return obj.following.is_certified

    def get_groups(self, obj):
        return obj.following.groups



class ProfileSearchSerializer(FollowerSerializer):

    def get_slug(self, obj):
        return obj.slug

    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.fullname

    def get_photo(self, obj):
        return obj.get_photo

    def get_icon_name(self, obj):
        return obj.icon_name

    def get_icon_color(self, obj):
        return obj.icon_color

    def get_is_anonymous(self, obj):
        return obj.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.is_dark_mode

    def get_is_verified(self, obj):
        return obj.is_verified

    def get_is_certified(self, obj):
        return obj.is_certified

    def get_groups(self, obj):
        return obj.groups



class Userv2Serializer(serializers.Serializer):
    slug =serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    icon_name = serializers.SerializerMethodField()
    icon_color = serializers.SerializerMethodField()
    full_name = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    is_verified = serializers.SerializerMethodField()
    is_certified = serializers.SerializerMethodField()

    is_anonymous = serializers.SerializerMethodField()
    is_dark_mode = serializers.SerializerMethodField()

    groups = serializers.SerializerMethodField()

    # more details maybe

    def get_slug(self, obj):
        return obj.slug

    def get_username(self, obj):
        return obj.user.username

    def get_full_name(self, obj):
        return obj.fullname

    def get_photo(self, obj):
        return obj.get_photo

    def get_is_verified(self, obj):
        return obj.is_verified

    def get_is_certified(self, obj):
        return obj.is_certified

    def get_is_anonymous(self, obj):
        return obj.is_anonymous

    def get_is_dark_mode(self, obj):
        return obj.is_dark_mode

    def get_groups(self, obj):
        return obj.groups

    def get_icon_name(self, obj):
        return obj.icon_name

    def get_icon_color(self, obj):
        return obj.icon_color


class Userv2WithProfileSerializer(Userv2Serializer):
    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        return ProfileSerializer(obj).data


class UserWithProfileSerializer(UserSerializer):
    profile = ProfileSerializer()


class CredentialSerializer(serializers.Serializer):
    token_type = serializers.CharField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    expires = serializers.DateTimeField()
    user = UserSerializer()


class ConnectionSerializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_user(self, obj):
        if obj.connector.slug == obj.user_slug:
            return Userv2Serializer(obj.connectee).data
        return Userv2Serializer(obj.connector).data


class Connectionv2Serializer(serializers.Serializer):
    user = serializers.SerializerMethodField()
    status = serializers.CharField()
    created_at = serializers.DateTimeField()

    def get_user(self, obj):
        return Userv2Serializer(obj.connector).data


class DocumentSerializer(serializers.Serializer):
    slug = serializers.CharField()
    type = serializers.CharField()
    file = serializers.FileField()
    description = serializers.CharField()
    remarks = serializers.CharField()
    created_at = serializers.DateTimeField()


class DocumentTypeSerializer(serializers.Serializer):
    text = serializers.CharField()


class ChatRoomSerializer(serializers.Serializer):
    slug = serializers.CharField()
    title = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    preview = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_title(self, obj):
        if obj.title: return obj.title
        if obj.members.count() < 2: return obj.members.all()[0].fullname

        members = obj.members.exclude(slug=obj.profile).values_list('fullname', flat=True)
        if obj.members.count() == 2:
            return members[0]

        title = " and ".join(members[0:2]) + " and "+ str(len(members)) + " others"
        return title

    def get_members(self, obj):
        return Userv2Serializer(obj.members, many=True).data

    def get_preview(self, obj):
        message_preview = obj.message_preview
        if message_preview:
            if message_preview.seen_by.filter(slug=obj.profile).exists():
                message_preview.seen_by.add(Profile.people.get(slug=obj.profile))
            message_preview.is_readed = True
            return MessageSerializer(message_preview).data


class MessageSerializer(serializers.Serializer):
    slug = serializers.CharField()
    chatroom_slug = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    is_readed = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_chatroom_slug(self, obj):
        return obj.chatroom.slug

    def get_created_by(self, obj):
        return Userv2Serializer(obj.created_by).data

    def get_text(self, obj):
        if obj.state == 'active': return obj.text
        return 'Removed by user'

    def get_is_readed(self, obj):
        if hasattr(obj, 'is_readed'): return obj.is_readed

import json

class NotificationSerializer(serializers.Serializer):
    slug = serializers.CharField()
    type = serializers.CharField()
    text = serializers.CharField()
    attrs_json = serializers.SerializerMethodField()
    is_readed = serializers.BooleanField()
    created_by = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField()

    def get_created_by(self, obj):
        return Userv2Serializer(obj.created_by).data

    def get_attrs_json(self, obj):
        return json.loads(obj.attrs_json)


class TagSerializer(serializers.Serializer):
    slug = serializers.CharField()
    text = serializers.CharField()
    num_count = serializers.CharField()