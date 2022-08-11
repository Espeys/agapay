import json
import importlib
import math

from apps.account.models import (
    ProfileFollower,
    ProfileConnection,
    Profile,
    Support,
    ChatRoom,
    Message,
    Notification,
    Activity
)
from apps.security.models import SourceToken
from base.models import (
    CHARFIELD_LONG_MAX_LENGTH as CLML,
    CHARFIELD_SHORT_MAX_LENGTH as CSML,
)
from base.encoders import ModelEncoder
from base import (
    utils as base_utils,
    forms as base_forms,
    fields as base_fields
)
from django import forms
from django.contrib.auth import get_user_model
from django.conf import settings as django_settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.utils import timezone
from django.template.loader import render_to_string
from django.db.models import Q, F, FloatField, IntegerField, Value, When, Case, Avg, CharField, Count
from django.db.models.functions import Cast
# geo

from . import models, serializers


User = get_user_model()


class BaseStaticForm(base_forms.BaseStaticForm):

    default_error_messages = {
        'invalid_filter': 20000,
        'invalid_filter_type': 20001,
        'invalid_page': 20002,
        'invalid_slug_query': '20003',
        'invalid_search': '20004',
        'invalid_order_values': 20005,
        'invalid_order_values_type': 20006,
        'invalid_query': '20007'
    }



from apps.account.recommendation import recommend

class RecommendPromotionsForm(BaseStaticForm):
    serializer_class = serializers.PostItemSerializer
    search_fields = [
        'description',
        'email',
        'weblink',
        'created_by__user__username',
        'created_by__fullname',
        'tags__text',
        'item_type',
        'promotion_type',
    ]
    list_filter = [
        'created_by__slug',
        'created_at__date',
        'created_at__month',
        'created_at__year',
        'miles__lte',
        'miles__gte',
        'miles__range'
        'is_verified',
        'item_type',
        'promotion_type',
        'help_type',
        'mood_type',
    ]
    page_counter = -1
    order_list = ['created_at']

    def custom_count(self, qs):
        return len(qs)

    def get_queryset(self, view, request, *args, **kwargs):
        A = recommend.Aggregation(request.user.profile)
        R = recommend.Recommendation(A, request)

        # try:
        return R.content_recommend()
        #except: return R.err_recommend().exclude(created_by__slug=request.user.profile)


class RecommendEmptyForm(BaseStaticForm):
    serializer_class = serializers.PostItemSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):
        A = recommend.Aggregation(request.user.profile)
        R = recommend.Recommendation(A, request)

        # try:
        return R.content_recommend()
        # return R.err_recommend().exclude(created_by__slug=request.user.profile)



class PostsNewsFeedForm(BaseStaticForm):
    serializer_class = serializers.PostItemSerializer
    search_fields = [
        'description',
        'email',
        'weblink',
        'created_by__user__username',
        'created_by__fullname',
        'tags__text',
        'item_type',
        'promotion_type',
    ]
    list_filter = [
        'created_by__slug',
        'created_at__date',
        'created_at__month',
        'created_at__year',
        'miles__lte',
        'miles__gte',
        'miles__range'
        'is_verified',
        'item_type',
        'promotion_type',
        'help_type',
        'mood_type',
    ]
    page_counter = -1
    order_list = ['created_at']

    def _final_out(self, serialize_out, view, request, *args, **kwargs):
        serialize_out = super()._final_out(serialize_out)

        Activity.objects.create(
            type=Activity.TYPE_NEWSFEED_SEARCH,
            params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
            response_json=json.dumps(serialize_out),
            created_by=request.user.profile if not request.user.is_anonymous else None
        )
        return serialize_out

    def get_queryset(self, view, request, *args, **kwargs):

        ITEM_PROMOTION = 'promotion'
        ITEM_STATUS = 'status'
        ITEM_DIARY = 'diary'
        ITEM_REQUEST = 'request'
        ITEM_OFFER = 'offer'

        PROMOTION_CAMPAIGN = 'campaign'
        PROMOTION_EVENT = 'event'
        PROMOTION_HOTLINE = 'hotline'
        PROMOTION_SERVICE = 'service'
        PROMOTION_GROUP = 'group'
        PROMOTION_INITIATIVE = 'initiative'
        PROMOTION_ARTICLE = 'article'
        PROMOTION_ADS = 'ads'
        PROMOTION_OTHER = 'other'

        QS_TYPE_NEWSFEED = 'newsfeed'
        QS_TYPE_DIARY = 'diary'
        QS_TYPE_BOOKMARK = 'saved'
        QS_TYPE_OWNED = 'owned'
        QS_TYPE_OTHER_PROFILE = 'other-profile'

        # just shorcut for diary, bookmarks, and own post or other post query
        qs_type = request.data.get('qs_type', None)

        if request.user.is_anonymous: profile = None
        else: profile = request.user.profile

        if profile: slug = profile.slug
        else: slug = None

        # for community help, just put filter gte
        ip = base_utils.get_lat_long(request)
        if qs_type == QS_TYPE_DIARY:
            return models.PostItem.objects.state_active().filter(
                item_type=ITEM_DIARY
            ).annotate(
                miles=Value(
                    base_utils.get_distance(
                        ip,
                        base_utils.get_lat_long(F('geoip'))
                    ), output_field=FloatField()
                ),
                request=Value(slug, output_field=CharField())
            )

        qs = models.PostItem.objects.state_active().exclude(
            item_type=ITEM_DIARY
        ).annotate(
            miles=Value(
                base_utils.get_distance(
                    ip,
                    base_utils.get_lat_long(F('geoip'))
                ), output_field=FloatField()
            ),
            request=Value(slug, output_field=CharField())
        )

        if qs_type == QS_TYPE_OWNED:
            qs = qs.filter(created_by=request.user.profile)

        elif qs_type == QS_TYPE_BOOKMARK:
            return request.user.profile.bookmarks.filter(
                state=models.PostItem.STATE_ACTIVE).annotate(
                     miles=Value(
                    base_utils.get_distance(
                        ip,
                        base_utils.get_lat_long(F('geoip'))
                    ), output_field=FloatField()
                ),
                request=Value(slug, output_field=CharField())
            )

        elif qs_type == QS_TYPE_OTHER_PROFILE:
            qs = qs.exclude(is_anonymous=True) # then use created_by__slug

        elif qs_type == QS_TYPE_NEWSFEED:

            followers = ProfileFollower.objects.filter(
                follower=profile,
            ).values_list('following__id', flat=True)
            connections_1 = ProfileConnection.objects.filter(
                connectee=profile,
                status=ProfileConnection.STATUS_ACCEPTED,
                state=ProfileConnection.STATE_ACTIVE
            ).values_list('connector__id', flat=True)
            connections_2 = ProfileConnection.objects.filter(
                connector=profile,
                status=ProfileConnection.STATUS_ACCEPTED,
                state=ProfileConnection.STATE_ACTIVE
            ).values_list('connectee__id', flat=True)

            qs = qs.filter(
                    Q(created_by__in=followers) \
                    | Q(created_by__in=connections_1) \
                    | Q(created_by__in=connections_2) \
                    | Q(created_by__in=[profile])
                )
        return qs # just random without diary


class PostsAddForm(forms.Form):
    VISIBILITY_CHOICES = models.PostItem.VISIBILITY_CHOICES
    ITEM_CHOICES = models.PostItem.ITEM_CHOICES_PLUS
    PROMOTION_CHOICES = models.PostItem.PROMOTION_CHOICES
    MOOD_CHOICES = models.PostItem.MOOD_CHOICES

    name = forms.CharField(required=False)
    banner = forms.FileField(required=False)
    title = forms.CharField(required=False, max_length=CLML)
    description = forms.CharField()
    email = forms.CharField(required=False)
    weblink = forms.URLField(required=False)
    location = forms.CharField(required=False, max_length=CLML)
    tel_no = forms.CharField(required=False, max_length=CSML)
    mobile_no = forms.CharField(required=False, max_length=CSML)
    sched_start = forms.DateTimeField(required=False)
    sched_end = forms.DateTimeField(required=False)

    # visibility_type = forms.ChoiceField(choices=VISIBILITY_CHOICES)
    item_type = forms.ChoiceField(choices=ITEM_CHOICES)
    promotion_type = forms.ChoiceField(choices=PROMOTION_CHOICES, required=False)
    censorship = forms.BooleanField(initial=False, required=False)
    # is_anonymous = forms.BooleanField(initial=False, required=False)
    help_type = forms.ChoiceField(choices=models.PostItem.HELP_CHOICES, required=False)
    mood_type = forms.ChoiceField(choices=MOOD_CHOICES, required=False)
    tags = base_fields.ArrayField(required=False)

    def __init__(self, *args, **kwargs):
        item_type = kwargs.pop('item_type')
        super().__init__(*args, **kwargs)

        if item_type.lower() == models.PostItem.ITEM_TYPE_PROMOTION:
            self.fields['promotion_type'].required = True
            self.fields.pop('mood_type')
            self.fields.pop('help_type')

        elif item_type.lower() == models.PostItem.ITEM_TYPE_DIARY:
            self.fields['mood_type'].required = True
            self.fields.pop('promotion_type')
            self.fields.pop('help_type')

        elif item_type.lower() in [models.PostItem.ITEM_TYPE_REQUEST,
            models.PostItem.ITEM_TYPE_OFFER]:
            self.fields['help_type'].required = True
            self.fields.pop('mood_type')
            self.fields.pop('promotion_type')
        else:
            self.fields.pop('mood_type')
            self.fields.pop('promotion_type')
            self.fields.pop('help_type')

    def handle(self, view, request, *args, **kwargs):
        now = timezone.now()
        data = self.cleaned_data

        tags = data.pop('tags')

        data['state'] = models.PostItem.STATE_ACTIVE
        data['created_by'] = request.user.profile
        data['is_anonymous'] = request.user.profile.is_anonymous

        data['geoip'] = base_utils.get_ip(request)
        coord = base_utils.get_lat_long(request)
        data['geo_lat'], data['geo_long'] = coord
        data['geo_full_address'] = base_utils.get_geo_address(request)

        # if data['item_type'].lower() == models.PostItem.ITEM_TYPE_DIARY \
        #     and models.PostItem.objects.state_active().filter(
        #         created_by=data['created_by'],
        #         created_at__date=now,
        #     ).count()>=1:
        #     # check if posted already today
        #     raise ValidationError('20011')

        obj = models.PostItem.objects.create(**data)

        obj.tags.clear()
        for tag in tags:
            t, c = models.PostTag.objects.get_or_create(text=tag)
            obj.tags.add(t)

        obj.miles = base_utils.get_distance(coord,coord)
        obj.request = request.user.profile.slug

        obj.create_log(
            action=models.PostItem.ADD_POST,
            from_attrs=json.dumps(obj, cls=ModelEncoder),
            profile=request.user.profile
        )

        serialized = serializers.PostItemSerializer(obj).data
        Activity.objects.create(
            type=Activity.TYPE_POST_ADD,
            params_json=json.dumps({}, cls=ModelEncoder),
            response_json=json.dumps({
                    'slug': serialized['slug'],
                    'created_by_slug': serialized['created_by']['slug']
                }, cls=ModelEncoder),
            created_by=request.user.profile
        )

        return serialized


class PostsEditForm(forms.Form):
    VISIBILITY_CHOICES = models.PostItem.VISIBILITY_CHOICES
    ITEM_CHOICES = models.PostItem.ITEM_CHOICES_PLUS

    slug = forms.CharField()
    banner = forms.FileField(required=False)
    name = forms.CharField(required=False, max_length=CLML)
    title = forms.CharField(required=False, max_length=CLML)
    description = forms.CharField(required=False)
    email = forms.CharField(required=False)
    weblink = forms.URLField(required=False)
    location = forms.CharField(required=False, max_length=CLML)
    tel_no = forms.CharField(required=False, max_length=CSML)
    mobile_no = forms.CharField(required=False, max_length=CSML)
    sched_start = forms.DateTimeField(required=False)
    sched_end = forms.DateTimeField(required=False)

    visibility_type = forms.ChoiceField(choices=VISIBILITY_CHOICES)
    item_type = forms.ChoiceField(choices=ITEM_CHOICES)
    censorship = forms.BooleanField(initial=False, required=False)
    is_anonymous = forms.BooleanField(initial=False, required=False)

    is_remove = forms.BooleanField(initial=False, required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                created_by=request.user.profile,
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        # logs
        from_attrs = json.dumps(post, cls=ModelEncoder)

        is_remove = data.pop('is_remove')
        banner = data.pop('banner')
        for k, v in data.items():
            if v in EMPTY_VALUES: setattr(post, k, v)

        post.is_verified = False
        if is_remove: post.banner = None
        if banner: post.banner = banner
        post.save()

        post.create_log(
            action=models.PostItem.EDIT_POST,
            from_attrs=from_attrs,
            profile=request.user.profile
        )
        return serializers.PostItemSerializer(post).data


class PostsDeleteForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                created_by=request.user.profile,
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        from_attrs = json.dumps(post, cls=ModelEncoder)
        post.state = models.PostItem.STATE_INACTIVE
        post.save()

        post.create_log(
            action=models.PostItem.DELETE_POST,
            from_attrs=from_attrs,
            profile=request.user.profile
        )

        return True


class PostsBookmarkForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        request.user.profile.bookmarks.add(post)

        post.miles= base_utils.get_distance(
            base_utils.get_lat_long(request),
            (post.geo_lat, post.geo_long)
        )
        post.request = request.user.profile.slug

        # add to the user
        return serializers.PostItemSerializer(post).data


class PostsUnbookmarkForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        request.user.profile.bookmarks.remove(post)

        # add to the user
        post.miles= base_utils.get_distance(
            base_utils.get_lat_long(request),
            (post.geo_lat, post.geo_long)
        )
        post.request = request.user.profile.slug

        # add to the user
        return serializers.PostItemSerializer(post).data


class PostsLikeForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        post.likes.add(request.user.profile)

        post.miles = base_utils.get_distance(
            base_utils.get_lat_long(request),
            (post.geo_lat, post.geo_long)
        )
        post.request = request.user.profile.slug
        serialized = serializers.PostItemSerializer(post).data

        # Activity.objects.create(
        #     type=Activity.TYPE_POST_LIKE,
        #     params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
        #     response_json=json.dumps(serialized, cls=ModelEncoder),
        #     created_by=request.user.profile
        # )
        return serialized


class PostsUnlikeForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        post.likes.remove(request.user.profile)
        post.miles = base_utils.get_distance(
            base_utils.get_lat_long(request),
            (post.geo_lat, post.geo_long)
        )
        post.request = request.user.profile.slug
        return serializers.PostItemSerializer(post).data


class PostsReportForm(forms.Form):
    slug = forms.CharField()
    reason = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        data['post'] = post
        data['reported_by'] = request.user.profile

        models.PostReport.objects.create(**data)
        return True


class PostsHistoryForm(BaseStaticForm):
    serializer_class = serializers.PostHistorySerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):
        try:
            return models.PostAuditTrail.objects.filter(
                post__slug=kwargs.get('slug'),
                post__created_by=request.user.profile,
                state=models.PostAuditTrail.STATE_ACTIVE
            )
        except:
            return models.PostAuditTrail.objects.none()


class PostsReportedForm(BaseStaticForm):
    serializer_class = serializers.PostReportSerializer
    page_counter = -1

    def get_queryset(self, *args, **kwargs):
        return models.PostReport.objects.filter(
            post__state=models.PostReport.STATE_ACTIVE,
            state=models.PostReport.STATE_ACTIVE
        )


# moderator
class PostsCensorForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        post.censorship = True
        post.save()
        return serializers.PostItemSerializer(post).data


class PostsDiscardForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        post.state = models.PostItem.STATE_INACTIVE
        post.save()
        return True


class PostsLikersForm(BaseStaticForm):
    serializer_class = serializers.UserSerializer
    page_counter = -1

    def get_queryset(self, *args, **kwargs):
        try:
            post = models.PostItem.objects.get(
                slug=kwargs.get('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
            return post.likes.state_active()
        except:
            return Profile.people.none()


class PostsVerifyForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        post = None
        try:
            post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        post.is_verified = True
        post.save()
        return True


class PostsShareForm(forms.Form):
    VISIBILITY_CHOICES = models.PostItem.VISIBILITY_CHOICES
    ITEM_CHOICES = models.PostItem.ITEM_CHOICES_PLUS

    slug = forms.CharField()
    description = forms.CharField()
    # visibility_type = forms.ChoiceField(choices=VISIBILITY_CHOICES)
    item_type = forms.ChoiceField(choices=ITEM_CHOICES)
    help_type = forms.ChoiceField(choices=models.PostItem.HELP_CHOICES, required=False)
    censorship = forms.BooleanField(required=False, initial=False)
    # is_anonymous = forms.BooleanField(required=False, initial=False)

    def __init__(self, *args, **kwargs):
        item_type = kwargs.pop('item_type')
        super().__init__(*args, **kwargs)

        if item_type.lower() in [models.PostItem.ITEM_TYPE_OFFER,
        models.PostItem.ITEM_TYPE_REQUEST]:
            self.fields['help_type'].required=False
        else: self.fields.pop('help_type')

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        profile = request.user.profile
        shared_post = None
        try:
            shared_post = models.PostItem.objects.get(
                slug=data.pop('slug'),
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        # get the main post
        if shared_post.shared_post: shared_post = shared_post.shared_post

        if models.PostItem.objects.state_active(
            ).filter(
                shared_post=shared_post,
                created_by= profile
            ).count() == 1: raise ValidationError('20009')

        data['shared_post'] = shared_post
        data['created_by'] = profile
        data['is_anonymous'] = profile.is_anonymous

        data['geoip'] = base_utils.get_ip(request)
        coord = base_utils.get_lat_long(request)
        data['geo_lat'], data['geo_long'] = coord
        data['geo_full_address'] = base_utils.get_geo_address(request)

        obj = models.PostItem.objects.create(**data)

        obj.miles = 123123
        obj.request = 'dasdasd'

        # should be async, but oh well
        for follower in ProfileFollower.objects.filter(
            following=profile,state=ProfileFollower.STATE_ACTIVE):

            profile.create_notif(
                type=Notification.TYPE_POST,
                attrs_json=json.dumps({'post_slug': str(obj.slug)}),
                text='{name} shared a post: {description}'.format(
                        name=profile.fullname,
                        description=obj.description
                    ),
                notified_to=follower.follower
            )

        for connection in ProfileConnection.objects.filter(
            connector=profile, status= ProfileConnection.STATUS_ACCEPTED,
            state=ProfileConnection.STATE_ACTIVE
        ):
            profile.create_notif(
                type=Notification.TYPE_POST,
                attrs_json=json.dumps({'post_slug': str(obj.slug)}),
                text='{name} shared a post: {description}'.format(
                        name=profile.fullname,
                        description=obj.description
                    ),
                notified_to=connection.connectee
            )

        for connection in ProfileConnection.objects.filter(
            connectee=profile, status= ProfileConnection.STATUS_ACCEPTED,
            state=ProfileConnection.STATE_ACTIVE
        ):
            profile.create_notif(
                type=Notification.TYPE_POST,
                attrs_json=json.dumps({'post_slug': str(obj.slug)}),
                text='{name} shared a post: {description}'.format(
                        name=profile.fullname,
                        description=obj.description
                    ),
                notified_to=connection.connector
            )

        serialized = serializers.PostItemSerializer(obj).data
        Activity.objects.create(
            type=Activity.TYPE_POST_SHARE,
            params_json=json.dumps({}, cls=ModelEncoder),
            response_json=json.dumps({
                    'slug': serialized['slug'],
                    'created_by_slug': serialized['created_by']['slug'],
                    'shared_post_slug': serialized['shared_post']['slug'],
                    'shared_created_by_slug': serialized['shared_post']['created_by']['slug']
                }, cls=ModelEncoder),
            created_by=request.user.profile
        )
        return serialized


class PostCommentsForm(BaseStaticForm):
    serializer_class = serializers.CommentSerializer
    page_counter = -1

    def custom_count(self, qs):
        return models.PostComment.objects.filter(
                post__slug=self.kwarg_slug,
                post__state=models.PostItem.STATE_ACTIVE,
                state=models.PostComment.STATE_ACTIVE
            ).count()

    def get_queryset(self, view, request, *args, **kwargs):
        self.kwarg_slug = kwargs.get('slug')
        profile = request.user.profile

        comments = models.PostComment.objects.filter(
            post__slug=self.kwarg_slug,
            post__state=models.PostItem.STATE_ACTIVE,
            parent=None,
            state=models.PostComment.STATE_ACTIVE
        ).annotate(
            user_comment = Case(When(created_by=profile, then=Value(1)),
            default=Value(0),
            output_field=IntegerField()
            )
        ).order_by('-user_comment', '-updated_at')
        return comments


class PostCommentAddForm(forms.Form):
    slug = forms.CharField() # post
    parent_slug = forms.CharField(required=False)
    description = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        profile = request.user.profile

        try:
            post = models.PostItem.objects.state_active().get(
                slug=data.pop('slug')
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20008')

        data['post'] = post
        data['created_by'] = profile
        data['is_anonymous'] = profile.is_anonymous

        parent = data.pop('parent_slug')
        if parent:
            try:
                base_comment = models.PostComment.objects.get(
                    slug=parent,
                    post=post,
                    state=models.PostComment.STATE_ACTIVE
                )
            except: raise ValidationError('20012')
            if base_comment.parent: raise ValidationError('20013')
            data['parent'] = base_comment
        comment = models.PostComment.objects.create(**data)

        serialized = serializers.CommentSerializer(comment).data

        Activity.objects.create(
            type=Activity.TYPE_POST_COMMENT,
            params_json=json.dumps({}, cls=ModelEncoder),
            response_json=json.dumps({
                    'slug': post.slug,
                    'created_by_slug': post.created_by.slug
                }),
            created_by=request.user.profile if not request.user.is_anonymous else None
        )
        return serialized


class PostCommentEditForm(forms.Form):
    slug = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        profile = request.user.profile

        try:
            comment = models.PostComment.objects.get(
                slug=data.pop('slug'),
                post__state=models.PostItem.STATE_ACTIVE,
                created_by=profile,
                state=models.PostComment.STATE_ACTIVE
            )
        except models.PostComment.DoesNotExist:
            raise ValidationError('20014')

        comment.is_anonymous = profile.is_anonymous
        comment.description = data['description']
        comment.save()

        return serializers.CommentSerializer(comment).data


class PostCommentDeleteForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        profile = request.user.profile

        try:
            comment = models.PostComment.objects.get(
                slug=data.pop('slug'),
                created_by=profile,
                state=models.PostComment.STATE_ACTIVE
            )
        except models.PostComment.DoesNotExist:
            raise ValidationError('20014')
        comment.state = comment.STATE_INACTIVE
        comment.save()
        return True


class PostCommentReportForm(forms.Form):
    slug = forms.CharField()
    reason = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        profile = request.user.profile

        try:
            comment = models.PostComment.objects.get(
                slug=data.pop('slug'),
                created_by=profile,
                state=models.PostComment.STATE_ACTIVE
            )
        except models.PostComment.DoesNotExist:
            raise ValidationError('20014')
        data['comment'] = comment
        data['reported_by'] = profile
        models.PostCommentReport.objects.create(**data)
        return True


class AccountsMoodContentForm(BaseStaticForm):
    serializer_class = serializers.MoodSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):

        try:
            return models.PostItem.objects.state_active().filter(
                created_by=request.user.profile,
                item_type=models.PostItem.ITEM_MOOD,
            )
        except Exception as e:
            return models.PostItem.objects.none()


class AccountsMoodAddForm(forms.Form):
    mood = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        data['profile'] = request.user.profile
        now = timezone.now()

        if not models.PostItem.objects.filter(
                created_by=data['profile'],
                item_type=models.PostItem.ITEM_MOOD,
                updated_at__range=[
                    now-timezone.timedelta(hours=24),
                    now+timezone.timedelta(hours=24)
                ]
            ).exists():

            obj = models.MoodTrack.objects.create(**data)
            return serializers.MoodSerializer(obj).data

        raise ValidationError('20010')


class AccountsMoodEditForm(forms.Form):
    slug = forms.CharField()
    mood = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        data['profile'] = request.user.profile
        now = timezone.now()

        try:
            obj = models.MoodTrack.objects.get(
                slug=data['slug'],
                created_by=data['profile'],
                item_type=models.PostItem.ITEM_MOOD,
                updated_at__range=[
                    now-timezone.timedelta(hours=24),
                    now+timezone.timedelta(hours=24)
                ]
            )

            for k, v in data.items():
                if v in EMPTY_VALUES: setattr(obj, k, v)
            obj.save()

            return serializers.MoodSerializer(obj).data
        except Exception as e:
            raise ValidationError('20010')



class PostTagSaveForm(forms.Form):
    """
    Served as an add or update of skills in a position.
    @param skills: (list) of str
    @out (list) of str - Skills.
    """
    slug = forms.CharField(error_messages={'required': 20000})
    tags = base_fields.TypedJSONField(
            type=list,
            error_messages={
                'required': 20000,
                'invalid': 20000,
                'invalid_type': 20000,
            }
        )

    def clean_skills(self):
        tags = self.cleaned_data['tags']

        if tags \
            and not all(isinstance(tags, (str, int, float, bool)) for tag in tags):
            raise ValidationError('20000')

        if tags \
            and not all(len(tag) <= CSML for tag in tags):
            raise ValidationError('20000')

        return list(map(str.lower, tags))

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        tags = data['tags']

        try:
            post = models.PostItem.objects.get(
                slug=data['slug'],
                state=models.PostItem.STATE_ACTIVE
            )
        except models.PostItem.DoesNotExist:
            raise ValidationError('20000')

        # clear first. so incase deletion. Just pass an empty list.
        post.tags.clear()

        if tags:
            for tag in tags:
                p, c = models.PostTag.objects.get_or_create(name=post)
                post.tags.add(p)

        return serializers.PostTagSerializer(post.tags, many=True).data


MOOD_STATS_DICT = models.PostItem.MOOD_STATS

class AccountsDiaryAggregateForm(forms.Form):

    def handle(self, view, request, *args, **kwargs):

        now = timezone.now()
        current_week = now.today().isocalendar()[1]

        diaries = models.PostItem.objects.state_active(
            ).filter(
                Q(item_type=models.PostItem.ITEM_TYPE_DIARY) \
                & Q(created_by=request.user.profile) \
                & Q(created_at__week=current_week) \
                & Q(created_at__year=now.year)
            ).annotate(
                weight=Case(
                    When(mood_type=models.PostItem.MOOD_ANGRY, then=Value(1)),
                    When(mood_type=models.PostItem.MOOD_SAD, then=Value(2)),
                    When(mood_type=models.PostItem.MOOD_MEH, then=Value(3)),
                    When(mood_type=models.PostItem.MOOD_SATISFIED, then=Value(4)),
                    When(mood_type=models.PostItem.MOOD_HAPPY, then=Value(5)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            ).aggregate(average=Avg('weight'))

        ceil = math.ceil(diaries['average'])

        for k, v in MOOD_STATS_DICT.items():
            if v == ceil: return serializers.DiaryAggregateSerializer(
                    {   'weight': ceil,
                        'mood': k
                    }
                ).data


class PostsSupportSendForm(forms.Form):
    slugs = base_fields.ArrayField()
    post_slug = forms.CharField()
    reason = forms.CharField(required=False)
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        slugs = data.pop('slugs') if data['slugs'] else []

        post = None
        try:
            post = models.PostItem.objects.state_active().get(slug=data.pop('post_slug'))
        except: raise ValidationError('20008')

        for slug in slugs:
            if not Profile.people.state_active().filter(slug=slug).exists():
                raise ValidationError('20015')
        profiles = Profile.people.state_active().filter(slug__in=slugs)

        support = Support.objects.create(
                attrs_json=json.dumps(
                {'post_slug': post.slug}
            ), type=Support.TYPE_POST, **data)

        for prof in profiles:
            prof.supports.add(support)

            request.user.profile.create_notif(
                type=Notification.TYPE_SUPPORT,
                attrs_json=json.dumps({'support_slug': str(support.slug)}),
                text='{name} had requested a support.'.format(name=request.user.profile.fullname),
                notified_to=prof
            )

        support.ip = base_utils.get_ip(request)
        support.request = request.user.profile

        serialized = serializers.PostSupportSerializer(support).data

        Activity.objects.create(
            type=Activity.TYPE_POST_SUPPORT_REQUEST,
            params_json=json.dumps({'user_slugs': slugs}, cls=ModelEncoder),
            response_json=json.dumps({
                    'slug': post.slug,
                    'created_by_slug': post.created_by.slug
                }),
            created_by=request.user.profile if not request.user.is_anonymous else None
        )

        return serialized


class PostsSupportsForm(BaseStaticForm):
    serializer_class = serializers.PostSupportSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):
        return request.user.profile.supports.filter(
                state=Support.STATE_ACTIVE,
                status=Support.STATUS_PENDING).annotate(
                ip=Value(base_utils.get_ip(request), CharField()),
                request=Value(request.user.profile.slug, CharField())
            )


class PostsSupportAcceptForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):

        try:
            support = request.user.profile.supports.get(
                slug=self.cleaned_data.get('slug'),
                state=Support.STATE_ACTIVE,
                status=Support.STATUS_PENDING
            )
        except: raise ValidationError('20016')

        # message

        post_slug = json.loads(support.attrs_json)['post_slug']
        support_user = models.PostItem.objects.filter(slug=post_slug
            ).first().created_by

        user_slugs = list({support_user, request.user.profile})
        chatroom = ChatRoom.objects.filter(
            members__in=user_slugs
        ).annotate(num_count=Count('members')
        ).filter(num_count=len(user_slugs))

        for user in user_slugs: chatroom = chatroom.filter(members__in=[user])
        if chatroom.exists(): chatroom = chatroom.first()
        else:
            chatroom = ChatRoom.objects.create()
            for user in user_slugs: chatroom.members.add(user)
        chatroom.profile = request.user.profile

        message = Message.objects.create(
            chatroom = chatroom,
            text="Hi, someone flagged your post that you need help. How can we help you?",
            created_by=request.user.profile
        )

        request.user.profile.create_notif(
            type=Notification.TYPE_CHATROOM,
            attrs_json=json.dumps({'chatroom_slug': str(chatroom.slug)}),
            text='{name} had accepted your support request. View your message.'.format(
                name=request.user.profile.fullname),
            notified_to=support_user
        )

        support.status = Support.STATUS_ACCEPTED
        support.save()

        Activity.objects.create(
            type=Activity.TYPE_POST_SUPPORT_ACCEPT,
            params_json=json.dumps({}, cls=ModelEncoder),
            response_json=json.dumps({
                    'slug': post_slug,
                    'created_by_slug': support_user.slug
                }, cls=ModelEncoder),
            created_by=request.user.profile
        )

        # chatroom
        return serializers.ChatRoomSerializer(chatroom).data


class PostsSupportDeclineForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):

        try:
            support = request.user.profile.supports.get(
                slug=self.cleaned_data.get('slug'),
                state=Support.STATE_ACTIVE,
                status=Support.STATUS_PENDING
            )
        except: raise ValidationError('20016')
        support.status = Support.STATUS_DENIED
        support.save()
        return True