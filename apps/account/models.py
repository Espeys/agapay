import uuid

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from django.db.models import Q

from . import generators

# Create your models here.


class ProfileQuerySet(models.QuerySet):

    def state_active(self):
        return self.filter(state=Profile.STATE_ACTIVE)

    def candidates(self):
        return self.filter(user__groups__name__in=[Profile.GROUP_CANDIDATE])

    def organizers(self):
        return self.filter(user__groups__name__in=[Profile.GROUP_ORGANIZER, Profile.GROUP_INDIVIDUAL])

    def common_groups(self):
        return self.filter(user__groups__name__in=[
            Profile.GROUP_CANDIDATE,
            Profile.GROUP_ORGANIZER,
            Profile.GROUP_INDIVIDUAL
        ])


class ProfileManager(models.Manager):

    def state_active(self):
        return self.get_queryset().state_active()

    def candidates(self):
        return self.get_queryset().state_active().candidates()

    def organizers(self):
        return self.get_queryset().state_active().organizers()

    def common_groups(self):
        return self.get_queryset().state_active().common_groups()


class ProfileFollowQuerySet(models.QuerySet):

    def state_active(self):
        return self.filter(state=ProfileFollower.STATE_ACTIVE)

class ProfileFollowManager(models.Manager):

    def state_active(self):
        return self.get_queryset().state_active()


class Profile(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    GROUP_CANDIDATE = 'regular'
    GROUP_ORGANIZER = 'organization'
    GROUP_INDIVIDUAL = 'provider'
    GROUP_MODERATOR = 'moderator'

    GROUP_LISTS = [
        GROUP_CANDIDATE,
        GROUP_ORGANIZER,
    ]

    GROUP_CHOICES = (
            ('candidate', GROUP_CANDIDATE),
            ('organizer', GROUP_ORGANIZER),
            ('individual', GROUP_INDIVIDUAL),
        )

    people = ProfileManager.from_queryset(ProfileQuerySet)()

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    #anonymotiy
    anonymous = models.CharField(default=generators.generate_anonymous_username, max_length=255, null=True, blank=True)
    icon_name = models.CharField(max_length=50, null=True, blank=True)
    icon_color = models.CharField(max_length=50, null=True, blank=True)

    photo = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    # contact_no = models.CharField(max_length=50, null=True, blank=True)
    tel_no = models.CharField(max_length=50, null=True, blank=True)
    mobile_no = models.CharField(max_length=50, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)

    service_type = models.CharField(max_length=50, null=True, blank=True)
    tags = models.ManyToManyField('post.PostTag', blank=True)

    # office_days
    office_start_time = models.TimeField(null=True, blank=True)
    office_end_time = models.TimeField(null=True, blank=True)

    # emergency
    emergency_contact_person = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact_number = models.CharField(max_length=255, null=True, blank=True)

    # bookmarks
    bookmarks = models.ManyToManyField('post.PostItem', blank=True)

    # candidate
    # group

    # documents
    documents = models.ManyToManyField('account.Document', blank=True)

    # followers
    followers = models.ManyToManyField(
        'self',
        through='account.ProfileFollower',
        through_fields=('follower', 'following'),
        symmetrical=False,
        blank=True,
        related_name='%(class)s_followers'
    )


    # connections = models.ManyToManyField(
    #     'self',
    #     through='account.ProfileConnection',
    #     through_fields=('connector', 'connectee'),
    #     symmetrical=True,
    #     blank=True,
    #     related_name='%(class)s_connections'
    # )
    # connections = models.ManyToManyField(
    #     'account.ProfileConnection',
    #     through='account.ProfileConnection',
    #     blank=True
    # )

    supports = models.ManyToManyField(
        'account.Support',
        blank=True
    )

    is_verified = models.BooleanField(default=False) # VERIFY EMAIL
    is_certified = models.BooleanField(default=False) # organization verified

    is_anonymous = models.BooleanField(default=False)
    is_dark_mode = models.BooleanField(default=False)


    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create_profile_user(cls, sender, instance, created, **kwargs):
        if created:
            profile = Profile._default_manager.create(user=instance)

    @property
    def get_photo(self):
        return self.photo.url if self.photo else None

    @property
    def groups(self):
        return [str(group) for group in self.user.groups.all().order_by('name')]

    @property
    def permissions(self):
        return self.user.get_user_permissions()

    @property
    def follower_count(self):
        return ProfileFollower.objects.filter(
            following=self,
            state=ProfileFollower.STATE_ACTIVE
        ).count()

    @property
    def following_count(self):
        return ProfileFollower.objects.filter(
            follower=self,
            state=ProfileFollower.STATE_ACTIVE
        ).count()

    @property
    def connection_count(self):
        return ProfileConnection.objects.filter(
            Q(Q(connector=self) | Q(connectee=self)) \
            & Q(state=ProfileConnection.STATE_ACTIVE) \
            & Q(status=ProfileConnection.STATUS_ACCEPTED)
        ).count()

    def create_notif(self, *args, **kwargs):
        return Notification.objects.create(created_by=self, *args, **kwargs)

    def __str__(self):
        return str(self.slug)

post_save.connect(Profile.create_profile_user, sender=settings.AUTH_USER_MODEL)


class ProfileFollower(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    follower = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='following')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class ProfileConnection(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive' # deny

    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'


    STATUS_CHOICES  = (
        ('accepted', STATUS_ACCEPTED),
        ('pending', STATUS_PENDING)
    )

    REQUEST_ACCEPT = 'accept'
    REQUEST_DENY = 'deny'

    REQUEST_CHOICES = (
        ('accept', REQUEST_ACCEPT),
        ('deny', REQUEST_DENY)
    )

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    connector = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='connector')
    connectee = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='connectee')

    status = models.CharField(max_length=50, default=STATUS_PENDING, null=True, blank=True)

    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)



# ??
class Message(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    from_user = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='follower')
    to_user = models.ForeignKey('account.Profile', on_delete=models.CASCADE, related_name='following')
    message = models.TextField(null=True, blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # abstract to not make a table
        abstract = True

    def __str__(self):
        return str(self.slug)


class ProfileReport(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    reported_to = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='reported')
    reason = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    reported_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='reportee')

    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class Support(models.Model):
    TYPE_POST = 'post-support'

    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    STATUS_PENDING = 'pending'
    STATUS_ACCEPTED = 'accepted'
    STATUS_DENIED = 'denied'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    attrs_json = models.TextField(null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    status = models.CharField(default=STATUS_PENDING, max_length=50, null=True, blank=True)

    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class DocumentType(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    text = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Document(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)

    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class ChatRoom(models.Model):
    """
        instances of chat
        to validate always is that, always check the slug and if user was there
    """
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    TYPE_PERSONAL = 'personal'
    TYPE_GROUP = 'group'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    title = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(default=TYPE_PERSONAL, max_length=50, null=True, blank=True)
    members = models.ManyToManyField('account.Profile', blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def message_preview(self):
        # message obj
        return Message.objects.filter(chatroom=self).order_by('-created_at').first()

    def __str__(self):
        return str(self.slug)


class Message(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    chatroom = models.ForeignKey('account.ChatRoom', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('account.Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='message_creator')
    seen_by = models.ManyToManyField('account.Profile', blank=True, related_name='seen_by')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class Notification(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    TYPE_POST = 'type-post'
    TYPE_FOLLOW = 'type-follow'
    TYPE_CONNECT = 'type-connect'
    TYPE_SUPPORT = 'type-support'
    TYPE_CHATROOM = 'type-chatroom'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    type = models.CharField(max_length=50,null=True, blank=True)
    attrs_json = models.TextField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    is_readed = models.BooleanField(default=False)
    notified_to = models.ForeignKey('account.Profile', on_delete=models.SET_NULL, null=True, blank=True, related_name='notifactee')
    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='notifactor')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class Activity(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    TYPE_PROFILE_SEARCH = 'profile-search'
    TYPE_NEWSFEED_SEARCH = 'newsfeed-search'
    # TYPE_CONNECT = 'type-connect'
    # TYPE_SUPPORT = 'type-support'
    # TYPE_CHATROOM = 'type-chatroom'
    TYPE_FOLLOW = 'follow'
    TYPE_CONNECT_REQUEST = 'connect-request'
    TYPE_CONNECT_ACCEPT = 'connect-accept'
    TYPE_POST_ADD = 'post-add'
    TYPE_POST_LIKE = 'post-like'
    TYPE_POST_SHARE = 'post-share'
    TYPE_POST_COMMENT = 'post-comment'
    TYPE_POST_SUPPORT_REQUEST = 'post-support-request'
    TYPE_POST_SUPPORT_ACCEPT = 'post-support-accept'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    type = models.CharField(max_length=50,null=True, blank=True)
    params_json = models.TextField(null=True, blank=True)
    response_json = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='activator')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)



# so list of messages in which wala pa sa simula
# then create convo if wala pa else join
# if iniated load all past chats
# then websocket current
# then check for unread
# give api that will make unread to read if toggled



# notif needed activity logs
# activity logs is used for recommendation
