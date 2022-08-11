import json
import uuid

from apps.account.models import Profile
from base.encoders import ModelEncoder

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class PostQuerySet(models.QuerySet):
    STATE_ACTIVE = 'active'

    def state_active(self):
        return self.filter(state=self.STATE_ACTIVE)


class PostManager(models.Manager):

    def state_active(self):
        return self.get_queryset().state_active()


class PostItem(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'


    VISIBILITY_PUBLIC = 'Public'
    VISIBILITY_PRIVATE = 'Private'

    VISIBILITY_CHOICES = (
        ('Public', VISIBILITY_PUBLIC),
        ('Private', VISIBILITY_PRIVATE),
    )

    ITEM_TYPE_PROMOTION = 'promotion'
    ITEM_TYPE_STATUS = 'status'
    ITEM_TYPE_DIARY = 'diary'
    ITEM_TYPE_REQUEST = 'request'
    ITEM_TYPE_OFFER = 'offer'

    ITEM_CHOICES_PLUS = (
        ('promotion', ITEM_TYPE_PROMOTION),
        ('status', ITEM_TYPE_STATUS),
        ('diary', ITEM_TYPE_DIARY),
        ('request', ITEM_TYPE_REQUEST),
        ('offer', ITEM_TYPE_OFFER),
    )

    PROMOTION_TYPE_CAMPAIGN = 'campaign'
    PROMOTION_TYPE_EVENT = 'event'
    PROMOTION_TYPE_HOTLINE = 'hotline'
    PROMOTION_TYPE_SERVICE = 'service'
    PROMOTION_TYPE_GROUP = 'group'
    PROMOTION_TYPE_INITIATIVE = 'initiative'
    PROMOTION_TYPE_ARTICLE = 'article'
    PROMOTION_TYPE_ADS = 'ads'
    PROMOTION_TYPE_OTHER = 'other'

    PROMOTION_CHOICES = (
        ('campaign', PROMOTION_TYPE_CAMPAIGN),
        ('event', PROMOTION_TYPE_EVENT),
        ('hotline', PROMOTION_TYPE_HOTLINE),
        ('service', PROMOTION_TYPE_SERVICE),
        ('group', PROMOTION_TYPE_GROUP),
        ('initiative', PROMOTION_TYPE_INITIATIVE),
        ('article', PROMOTION_TYPE_ARTICLE),
        ('ads', PROMOTION_TYPE_ADS),
        ('other', PROMOTION_TYPE_OTHER)
    )

    MOOD_ANGRY = 'angry'
    MOOD_SAD = 'sad'
    MOOD_MEH = 'meh'
    MOOD_SATISFIED = 'satisfied'
    MOOD_HAPPY = 'happy'

    MOOD_CHOICES = (
        ('angry', MOOD_ANGRY),
        ('sad', MOOD_SAD),
        ('meh', MOOD_MEH),
        ('satisfied', MOOD_SATISFIED),
        ('happy', MOOD_HAPPY),
    )

    HELP_SERVICES = 'services'
    HELP_TIME = 'time'
    HELP_GOODS = 'goods'
    HELP_INFORMATION = 'information'
    HELP_OTHERS = 'others'

    HELP_CHOICES = (
        ('services', HELP_SERVICES),
        ('help', HELP_TIME),
        ('goods', HELP_GOODS),
        ('information', HELP_INFORMATION),
        ('others', HELP_OTHERS)
    )

    ADD_POST = 'add-post'
    EDIT_POST = 'edit-post'
    DELETE_POST = 'delete-post'

    MOOD_STATS = {
        'Angry': 1,
        'Sad': 2,
        'Meh': 3,
        'Satisfied': 4,
        'Happy': 5
    }

    objects = PostManager.from_queryset(PostQuerySet)()

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    banner = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)

    # share_post
    shared_post = models.ForeignKey('self',
            on_delete=models.CASCADE, null=True, blank=True, related_name='child')

    # name of organization
    name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)

    # moods
    mood = models.CharField(max_length=50, null=True, blank=True)

    # org/can
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    weblink = models.URLField(null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    mobile_no = models.CharField(max_length=50, null=True, blank=True)
    tel_no = models.CharField(max_length=50, null=True, blank=True)

    # public, private
    visibility_type = models.CharField(default=VISIBILITY_PUBLIC, choices=VISIBILITY_CHOICES, max_length=255, null=True, blank=True)
    # type
    item_type = models.CharField(choices=ITEM_CHOICES_PLUS, max_length=255, null=True, blank=True)
    promotion_type = models.CharField(choices=PROMOTION_CHOICES, max_length=255, null=True, blank=True)
    help_type = models.CharField(choices=HELP_CHOICES, max_length=255, null=True, blank=True)

    mood_type = models.CharField(choices= MOOD_CHOICES, max_length=50, null=True, blank=True)

    censorship = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)

    sched_start = models.DateTimeField(null=True, blank=True)
    sched_end = models.DateTimeField(null=True, blank=True)

    geoip = models.CharField(max_length=50, null=True, blank=True)
    geo_lat = models.FloatField(default=0, null=True, blank=True)
    geo_long = models.FloatField(default=0, null=True, blank=True)
    geo_full_address = models.CharField(max_length=50, null=True, blank=True)

    # seen_by
    # comment
    # comments = models.ManyToManyField('post.PostComment', blank=True, related_name='comments')
    # reply

    # tagging
    tags = models.ManyToManyField('post.PostTag', blank=True)

    is_verified = models.BooleanField(default=False)

    likes = models.ManyToManyField('account.Profile', blank=True, related_name='likes')
    # shares = models.ManyToManyField('account.Profile', blank=True, related_name='shares')
    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True, related_name='created_by')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_banner(self):
        return self.banner.url if self.banner else None

    def create_log(self, action=None, description=None, profile=None, from_attrs=None, *args, **kwargs):
        log = PostAuditTrail.objects.create(
            post=self,
            action=action,
            description=description,
            created_by=profile,
            from_attrs=from_attrs,
            to_attrs=json.dumps(self, cls=ModelEncoder)
        )

        return log

    @property
    def share_count(self):
        return PostItem._default_manager.filter(shared_post=self).count()

    @property
    def like_count(self):
        return self.likes.count()

    @property
    def comment_count(self):
        return PostComment.objects.filter(
                post=self,
                state=PostComment.STATE_ACTIVE
            ).count()

    def __str__(self):
        return str(self.slug)


class PostReport(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    post = models.ForeignKey('post.PostItem', on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    reported_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True)

    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)


class PostAuditTrail(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    post = models.ForeignKey('post.PostItem', on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    from_attrs = models.TextField(null=True, blank=True)
    to_attrs = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)



class PostComment(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    post = models.ForeignKey('post.PostItem', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)



class PostTag(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    text = models.CharField(max_length=50, default=STATE_ACTIVE)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# commenting system  # note level 1 only atm
# mini recommender system
# track activity



class PostCommentReport(models.Model):
    STATE_ACTIVE = 'active'
    STATE_INACTIVE = 'inactive'

    slug = models.CharField(default=uuid.uuid4, max_length=40, editable=False, db_index=True)
    comment = models.ForeignKey('post.PostComment', on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    reported_by = models.ForeignKey('account.Profile', on_delete=models.CASCADE, null=True, blank=True)

    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)
