import json
import importlib

from apps.security.models import SourceToken
from apps.security.exceptions import InvalidTokenError

from apps.post.models import PostTag as ProfileTag

from base.models import (
    CHARFIELD_LONG_MAX_LENGTH as CLML,
    CHARFIELD_SHORT_MAX_LENGTH as CSML,
)
from base import (
    utils as base_utils,
    forms as base_forms,
    fields as base_fields
)
from base.encoders import ModelEncoder

from django import forms
from django.contrib.auth import (
    authenticate,
    login,
    get_user_model,
)
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import (
    get_default_password_validators,
    validate_password,
)
from django.conf import settings as django_settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.validators import EMPTY_VALUES
from django.db import transaction
from django.db.models import Q, F, CharField, Value, Count, BooleanField, ExpressionWrapper
from django.utils import timezone
from django.template.loader import render_to_string
from oauth2_provider.models import Application,RefreshToken,AccessToken
from oauth2_provider.settings import oauth2_settings as oset


from . import models, serializers, utils


User = get_user_model()


class BaseStaticForm(base_forms.BaseStaticForm):

    default_error_messages = {
        'invalid_filter': 10025,
        'invalid_filter_type': 10026,
        'invalid_page': 10027,
        'invalid_slug_query': '10028',
        'invalid_search': '10029',
        'invalid_order_values': 10030,
        'invalid_order_values_type': 10031,
        'invalid_query': '10032'
    }


class ProfileFollowerForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data['follower'] == cleaned_data['following']:
            raise ValidationError('Cannot add itself.')

    class Meta:
        model = models.ProfileFollower
        fields = '__all__'


class TokenForm(forms.Form):
    access_token_model = AccessToken
    application_model = Application
    application_name = django_settings.DEFAULT_APPLICATION_MODEL_NAME
    refresh_token_model = RefreshToken

    def get_application_name(self):
        if not self.application_name:
            raise ValueError('application_name must not be empty')
        return self.application_name

    def get_application_model(self):
        if not self.application_model:
            raise ValueError('application_model must not be empty')
        return self.application_model

    def get_access_token_model(self):
        if not self.access_token_model:
            raise ValueError('access_token_model must not be empty')
        return self.access_token_model

    def get_refresh_token_model(self):
        if not self.refresh_token_model:
            raise ValueError('refresh_token_model must not be empty')
        return self.refresh_token_model

    def generate_application(self):
        name = self.get_application_name()
        application, created = self.get_application_model().objects.get_or_create(name=name)
        return application

    def generate_token(self, refresh=True):
        """
        Generate token depends on the token involved
        if module was None use default oauthlib.common generator
        @param refresh (boolean) - tells whether to use oauthsettings Refresh Gen
        if available.
        """
        method = 'oauthlib.common.generate_token'
        if refresh and oset.REFRESH_TOKEN_GENERATOR :
            method = oset.REFRESH_TOKEN_GENERATOR
        elif not refresh and oset.ACCESS_TOKEN_GENERATOR :
            method = oset.ACCESS_TOKEN_GENERATOR
        module = importlib.import_module('.'.join(method.split('.')[0:-1]))
        func = getattr(module, method.split('.')[-1])
        return func()

    def get_expiration(self):
        # specific only for access_token
        return oset.ACCESS_TOKEN_EXPIRE_SECONDS

    def get_access_token(self, user, source_refresh_token=None):
        access_token = self.get_access_token_model().objects.create(
            user=user,
            source_refresh_token=source_refresh_token,
            application=self.generate_application(),
            expires=timezone.now() + timezone.timedelta(seconds=self.get_expiration()),
            token=self.generate_token(refresh=False)
        )
        return access_token

    def get_refresh_token(self, user, access_token):
        refresh_token = self.get_refresh_token_model().objects.create(
            user=user,
            application=self.generate_application(),
            access_token=access_token,
            token=self.generate_token(refresh=True),
        )
        return refresh_token

    def get_token(self, user, source_refresh_token=None):
        access_token = self.get_access_token(user, source_refresh_token)
        refresh_token = self.get_refresh_token(user, access_token)
        return (access_token, refresh_token)

    def revoke_all_token(self, user):
        # revoke all tokens connected to user
        # e.g refresh
        refresh_tokens = RefreshToken.objects.filter(
            user=user,
            revoked=None
        )

        for refresh in refresh_tokens:
            refresh.revoke()


class AccountsLoginForm(TokenForm):
    username = forms.EmailField()
    password = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        user = authenticate(
            request=request,
            username=data['username'],
            password=data['password'],
        )

        if user is None:
            raise ValidationError('10002')

        access_token, refresh_token = self.get_token(user)
        out = {
            'token_type': 'Bearer',
            'access': access_token,
            'refresh': refresh_token,
            'expires': access_token.expires,
            'user': user,
        }

        return serializers.CredentialSerializer(out).data


class AccountsAccessForm(TokenForm):

    def handle(self, view, request, *args, **kwargs):

        user = request.user
        try:
            access_token = AccessToken.objects.get(
                user=user,
                application=self.generate_application(),
                token=request.auth.token
            )
        except AccessToken.DoesNotExist:
            raise ValidationError('10007')

        out = {
            'token_type': 'Bearer',
            'access': access_token,
            'refresh': request.auth.refresh_token,
            'expires': access_token.expires,
            'user': user
        }
        return serializers.CredentialSerializer(out).data


class AccountsRefreshForm(TokenForm):

    refresh_token = forms.CharField()

    def handle(self, view, request, *args, **kwargs):

        data = self.cleaned_data

        try:
            current_refresh_token = RefreshToken.objects.get(
                token=data.get('refresh_token'),
                user=request.user,
                access_token__token=request.auth.token,
                application=self.generate_application()
            )
        except RefreshToken.DoesNotExist:
            raise ValidationError('10005')

        if current_refresh_token.revoked is not None:
            raise ValidationError('10006')

        # revoke current refresh (now old)
        current_refresh_token.revoke()

        # get the user for creating token
        user = request.user

        # get new access and refresh
        access_token, refresh_token = self.get_token(user, current_refresh_token)
        out = {
            'token_type': 'Bearer',
            'access': access_token,
            'refresh': refresh_token,
            'expires': access_token.expires,
            'user': user,
        }

        return serializers.CredentialSerializer(out).data


class AccountsRegisterForm(TokenForm):
    CANDIDATE  = models.Profile.GROUP_CANDIDATE
    SERVICE_ORGANIZER = models.Profile.GROUP_ORGANIZER
    SERVICE_INDIVIDUAL = models.Profile.GROUP_INDIVIDUAL

    username = forms.EmailField(max_length=150)

    # user_type = forms.ChoiceField(
    #     choices=models.Profile.GROUP_CHOICES
    # )

    first_name = forms.CharField(
        max_length=30,
        required=False
    )
    last_name = forms.CharField(
        max_length=30,
        required=False
    )
    company_name = forms.CharField(
        max_length=150,
        required=False
    )
    password = forms.CharField()
    # password2 = forms.CharField()

    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group')
        super().__init__(*args, **kwargs)

        self.group = group
        if self.group == self.SERVICE_ORGANIZER:
            self.fields['company_name'].required = True
        else:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True

    def validate_password(self, user):
        password = self.cleaned_data.get('password')
        error_list = []

        try:
            validate_password(password, user)
        except ValidationError as v:
            for message in v.messages:
                error_list.append(ValidationError(
                    '10010',
                    params={'error': message},
                )
            )
        if error_list:
            raise ValidationError(error_list)
        return password

    def create_user(self, commit=False):
        data = self.cleaned_data

        first_name, last_name = (data['first_name'], data['last_name'])
        if self.group == self.SERVICE_ORGANIZER:
            first_name, last_name = (data['company_name'], data['company_name'])

        user = User(
            username=data['username'],
            email=data['username'],
            first_name=first_name,
            last_name=last_name
        )
        # validate password here
        self.validate_password(user)

        if commit:
            user.set_password(data.get('password'))
            user.save()

            # put the user in candidate group

            name = self.CANDIDATE
            if self.group == self.SERVICE_INDIVIDUAL:
                name = self.SERVICE_INDIVIDUAL
            if self.group == self.SERVICE_ORGANIZER:
                name = self.SERVICE_ORGANIZER

            group, created = Group.objects.get_or_create(
                name=name
            )

            if self.group in [self.CANDIDATE, self.SERVICE_INDIVIDUAL]:
                user.profile.fullname = "{first_name} {last_name}".format(
                    first_name=data['first_name'],
                    last_name=data['last_name']
                )
            else: user.profile.fullname = data['company_name']
            user.profile.save()
            user.groups.add(group)

        return user

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')

        if utils.check_user_exists(username):
            raise ValidationError('10008')

        # if cleaned_data.get('password') != cleaned_data.get('password2'):
        #     raise ValidationError('10009')

    def send_mail(self, request, user):
        # domain
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        # sender, receiver, subject, body
        from_email = django_settings.DEFAULT_FROM_EMAIL
        to_email = user.email
        subject_template_name = 'email/account/register_subject.txt'
        email_template_name = 'email/account/register_body.html'

        # settings of user in dict form
        settings = {'user_id': user.id , 'user_email': user.email}

        # create token
        token = SourceToken().create_token(
            user=user,
            action=SourceToken.ACTION_REGISTRATION_OTP,
            length=SourceToken.EMAIL_SECURITY_TOKEN_LENGTH,
            settings=settings,
        )

        context = {
            'email': to_email,
            'domain': domain,
            'site': site_name,
            'token': token,
            'protocol': request.is_secure()
        }

        # making subject, body
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        # actual send
        base_utils.send_mail(from_email, [to_email], subject, body)

    def handle(self, view, request, *args, **kwargs):
        self.create_user(commit=False)
        try:
            with transaction.atomic():
                user = self.create_user(commit=True)
                # email
                self.send_mail(request, user)
        except Exception as e:
            raise Exception(e)

        # get token
        access_token, refresh_token = self.get_token(user)
        out = {
            'token_type': 'Bearer',
            'access': access_token,
            'refresh': refresh_token,
            'expires': access_token.expires,
            'user': user,
        }
        return serializers.CredentialSerializer(out).data


class AccountsVerifyEmailForm(TokenForm):

    token = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        # soft validate
        try:
            settings = SourceToken().verify_token(
                action=SourceToken.ACTION_REGISTRATION_OTP,
                code=data['token'],
                is_expire=False
            )
        except InvalidTokenError:
            raise ValidationError('10034')

        user = User.objects.get(id=settings['user_id'])

        # if the user had the same specs
        # if not ((user.id == settings['user_id']) \
        #      and (user.email == settings['user_email'])):
        #     raise ValidationError('10021')

        # another validation
        if user.profile.is_verified:
            raise ValidationError('10034')

        # success
        user.profile.is_verified = True
        user.profile.save()

        SourceToken().verify_token(
            action=SourceToken.ACTION_REGISTRATION_OTP,
            code=data['token'],
            created_by=user
        )

        # get new access and refresh
        access_token, refresh_token = self.get_token(user)
        out = {
            'token_type': 'Bearer',
            'access': access_token,
            'refresh': refresh_token,
            'expires': access_token.expires,
            'user': user
        }

        # login with updated user
        return serializers.CredentialSerializer(out).data

# resend

class AccountsProfileForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):

        slug = self.cleaned_data.get('slug', None)

        try:
            profile = models.Profile.people.state_active(
                ).prefetch_related('user').get(slug=slug)
        except models.Profile.DoesNotExist:
            raise ValidationError('10011')

        return serializers.Userv2WithProfileSerializer(profile).data


class AccountsProfileUpdateForm(forms.Form):
    # slug = forms.CharField()
    email = forms.EmailField(required=False)
    about = forms.CharField(required=False)
    bio = forms.CharField(required=False)
    location = forms.CharField(max_length=255, required=False)
    tel_no = forms.CharField(max_length=50, required=False)
    mobile_no = forms.CharField(max_length=50, required=False)
    website = forms.URLField(required=False)
    service_type = forms.CharField(max_length=50, required=False)
    emergency_contact_person = forms.CharField(max_length=255, required=False)
    emergency_contact_number = forms.CharField(max_length=255, required=False)
    tags = base_fields.ArrayField(required=False)
    icon_name = forms.CharField(max_length=50, required=False)
    icon_color = forms.CharField(max_length=50, required=False)

    def handle(self, view, request, *args, **kwargs):

        profile  = request.user.profile

        for k, v in self.cleaned_data.items():
            if k == 'tags':
                profile.tags.clear()
                if v:
                    for tag in v:
                        t, c = ProfileTag.objects.get_or_create(text=tag)
                        profile.tags.add(t)
                continue
            setattr(profile, k, v)
        profile.save()

        return serializers.Userv2WithProfileSerializer(profile).data


class AccountsProfileConfigForm(forms.Form):
    is_anonymous = forms.BooleanField(required=False)
    is_dark_mode = forms.BooleanField(required=False)

    def handle(self, view, request, *args, **kwargs):
        profile  = request.user.profile

        for k, v in self.cleaned_data.items():
            setattr(profile, k, v)
        profile.save()

        return serializers.Userv2WithProfileSerializer(profile).data


class AccountsProfilePhotoUploadForm(forms.Form):
    # slug = forms.CharField()
    photo = forms.ImageField()

    def handle(self, view, request, *args, **kwargs):
        profile = request.user.profile

        profile.photo = self.cleaned_data.get('photo')
        profile.save()
        return serializers.Userv2WithProfileSerializer(profile).data


class AccountsProfilePhotoRemoveForm(forms.Form):

    def handle(self, view, request, *args, **kwargs):
        profile = request.user.profile

        profile.photo = None
        profile.save()

        return True


class AccountsPasswordChangeForm(TokenForm):
    old_password = forms.CharField()
    new_password = forms.CharField()
    # confirm_password = forms.CharField()

    def validate_password(self, user):
        password = self.cleaned_data.get('new_password')
        error_list = []

        try:
            validate_password(password, user)
        except ValidationError as v:
            for message in v.messages:
                error_list.append(ValidationError('10018', params={'error': message}))

        if error_list:
            raise ValidationError(error_list)

        return password

    def handle(self, view, request, *args ,**kwargs):
        data = self.cleaned_data

        user = request.user
        if not user.check_password(data.get('old_password')):
            raise ValidationError('10019')

        # if data['new_password'] != data['confirm_password']:
        #     raise ValidationError('10020')

        self.validate_password(user)

        user.set_password(data['new_password'])
        user.save()

        self.revoke_all_token(user)

        return True


class AccountsPasswordForgotForm(TokenForm):
    username = forms.EmailField()

    def send_mail(self, request):
        # domain
        current_site = get_current_site(request)
        site_name = current_site.name
        domain = current_site.domain

        username = self.cleaned_data.get('username')

        from_email = django_settings.DEFAULT_FROM_EMAIL
        to_email = username
        subject_template_name = 'email/account/forgot_password_subject.txt'
        email_template_name = 'email/account/forgot_password_body.html'
        settings = {'user_email': username}

        # get user
        user = User.objects.filter(username=username).first()

        password = User.objects.make_random_password()
        if user:
            user.set_password(password)
            user.save(update_fields=['password'])
            self.revoke_all_token(user)

        # create token
        token = SourceToken().create_token(
            action=SourceToken.ACTION_CHANGE_PASSWORD_OTP,
            user=user,
            length=SourceToken.EMAIL_SECURITY_TOKEN_LENGTH,
            settings=settings,
        )

        context = {
            'email': to_email,
            'domain': domain,
            'site': site_name,
            'token': token,
            'password': password,
            'protocol': request.is_secure()
        }

        # making subject, body
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        # actual send
        base_utils.send_mail(from_email, [to_email], subject, body)

    def handle(self, view, request, *args, **kwargs):
        self.send_mail(request)
        return True


class AccountsPasswordForgotConfirmForm(TokenForm):
    token = forms.CharField()
    password = forms.CharField()
    # confirm_password = forms.CharField()

    def validate_password(self, user):
        password = self.cleaned_data.get('password')
        error_list = []

        try:
            validate_password(password, user)
        except ValidationError as v:
            for message in v.messages:
                error_list.append(ValidationError('10021', params={'error': message}))

        if error_list:
            raise ValidationError(error_list)
        return password

    def handle(self, view, *args, **kwargs):
        data = self.cleaned_data

        # if data['password'] != data['confirm_password']:
        #     raise ValidationError('10022')

        try:
            settings = SourceToken().verify_token(
                action=SourceToken.ACTION_CHANGE_PASSWORD_OTP,
                code=data['token'],
                is_expire=False,
            )
        except Exception:
            raise ValidationError('10023')

        user = None
        try:
            user = User.objects.get(username=settings['user_email'])
        except User.DoesNotExist:
            raise ValidationError('10023')

        self.validate_password(user)
        user.set_password(data['password'])
        user.save()

        self.revoke_all_token(user)

        # expires
        settings = SourceToken().verify_token(
            action=SourceToken.ACTION_CHANGE_PASSWORD_OTP,
            code=data['token']
        )
        return True


class AccountsProfileFollowForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        if slug == request.user.profile.slug:
            raise ValidationError('10024')

        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        request.user.profile.followers.add(profile)

        request.user.profile.create_notif(
            type = models.Notification.TYPE_FOLLOW,
            attrs_json = json.dumps({'from_slug': request.user.profile.slug }),
            text='{name} followed you'.format(name=request.user.profile.fullname),
            notified_to=profile
        )

        serialized = serializers.UserSerializer(profile.user).data

        models.Activity.objects.create(
            type = models.Activity.TYPE_FOLLOW,
            params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
            response_json=json.dumps(serialized, cls=ModelEncoder),
            created_by=request.user.profile
        )

        return serialized


class AccountsProfileUnfollowForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        if slug == request.user.profile.slug:
            raise ValidationError('10024')
        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        request.user.profile.followers.remove(profile)

        return True


class AccountsProfileFollowerForm(BaseStaticForm):
    serializer_class = serializers.FollowerSerializer
    page_counter = -1

    def get_queryset(self, *args, **kwargs):

        try:
            return models.ProfileFollower.objects.filter(
                following__slug=kwargs.get('slug'),
                state=models.ProfileFollower.STATE_ACTIVE
            )
        except:
            return models.ProfileFollower.objects.none()


class AccountsProfileFollowingForm(BaseStaticForm):
    serializer_class = serializers.FollowingSerializer
    page_counter = -1

    def get_queryset(self, *args, **kwargs):

        try:
            return models.ProfileFollower.objects.filter(
                follower__slug=kwargs.get('slug'),
                state=models.ProfileFollower.STATE_ACTIVE
            )
        except:
            return models.ProfileFollower.objects.none()


class AccountsOrganizerForm(BaseStaticForm):
    serializer_class = serializers.Userv2Serializer

    def get_serializer_class(self, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        serializer_class = super().get_serializer_class(*args, **kwargs)

        if slug:
            return serializers.Userv2WithProfileSerializer
        return serializer_class

    def get_queryset(self, *args, **kwargs):
        return models.Profile.people.organizers()


class AccountsOrganizerVerifyForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')

        try:
            profile = models.Profile.people.organizers().get(
                slug=slug,
                is_certified=False
            )
        except:
            raise ValidationError('10011')

        profile.is_valid = True
        profile.save()
        return serializers.Userv2WithProfileSerializer(profile).data


# connections

class AccountsConnectionRequestForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        if slug == request.user.profile.slug:
            raise ValidationError('10035')

        # requested profile
        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        # should be only one request for the for the requester
        # allows opposite to request to him also.
        if models.ProfileConnection.objects.filter(
                connector=request.user.profile,
                connectee=profile,
                status=models.ProfileConnection.STATUS_PENDING,
                state=models.ProfileConnection.STATE_ACTIVE # not denied
            ).exists():
            raise ValidationError('10037')

        # already friend
        if models.ProfileConnection.objects.filter(
                connector=profile,
                connectee=request.user.profile,
                status=models.ProfileConnection.STATUS_ACCEPTED,
                state=models.ProfileConnection.STATE_ACTIVE).exists() \
        and models.ProfileConnection.objects.filter(
                connectee=profile,
                connector=request.user.profile,
                status=models.ProfileConnection.STATUS_ACCEPTED,
                state=models.ProfileConnection.STATE_ACTIVE).exists(
            ): raise ValidationError('10042')

        obj = models.ProfileConnection.objects.create(
            connector=request.user.profile,
            connectee=profile
        )
        obj.user_slug = request.user.profile.slug

        serialized = serializers.ConnectionSerializer(obj).data

        models.Activity.objects.create(
            type=models.Activity.TYPE_CONNECT_REQUEST,
            params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
            response_json=json.dumps(serialized, cls=ModelEncoder),
            created_by=request.user.profile
        )
        return serialized


class AccountsConnectionRemoveForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        now = timezone.now()

        if slug == request.user.profile.slug:
            raise ValidationError('10035')

        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        # inactivate any from request side
        models.ProfileConnection.objects.filter(
                connector=request.user.profile, # one that requested
                connectee__slug=slug,
                state=models.ProfileConnection.STATE_ACTIVE
        ).update(
            state=models.ProfileConnection.STATE_INACTIVE,
            updated_at=now
        )

        # inactivate any from the other side
        models.ProfileConnection.objects.filter(
                connector__slug=slug, # one that requested
                connectee=request.user.profile,
                state=models.ProfileConnection.STATE_ACTIVE
            ).update(
                state=models.ProfileConnection.STATE_INACTIVE,
                updated_at=now
            )
        # remove each other
        # request.user.profile.connections.remove(profile)
        # profile.connections.remove(request.user.profile)

        return True


class AccountsConnectionStatusForm(forms.Form):
    slug = forms.CharField()
    status = forms.ChoiceField(choices=models.ProfileConnection.REQUEST_CHOICES)

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        status = self.cleaned_data.get('status').lower() # brute

        profile = request.user.profile
        connection = None
        # request
        try:
            connection = models.ProfileConnection.objects.get(
                connector__slug=slug,
                connectee=profile,
                status=models.ProfileConnection.STATUS_PENDING,
                state=models.ProfileConnection.STATE_ACTIVE
            )
        except Exception as e:
            raise ValidationError('10011')

        if status == models.ProfileConnection.REQUEST_ACCEPT:
            connection.status = models.ProfileConnection.STATUS_ACCEPTED
            connection.save()

            # inactivate other party
            models.ProfileConnection.objects.filter(
                connector=request.user.profile, # one that requested
                connectee__slug=slug,
                status=models.ProfileConnection.STATUS_PENDING,
                state=models.ProfileConnection.STATE_ACTIVE
            ).update(
                state=models.ProfileConnection.STATE_INACTIVE,
                updated_at=timezone.now()
            )

            # connect each other

            other_profile = models.Profile.people.get(slug=slug)

            other_profile.create_notif(
                type = models.Notification.TYPE_CONNECT,
                attrs_json = json.dumps({'from_slug': other_profile.slug }),
                text='{name} accepted your request'.format(name=other_profile.fullname),
                notified_to=profile
            )

            # accept is valuable
            models.Activity.objects.create(
                type=models.Activity.TYPE_CONNECT_ACCEPT,
                params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
                response_json=json.dumps(serializers.Userv2Serializer(other_profile).data,
                    cls=ModelEncoder),
                created_by=request.user.profile
            )


        elif status == models.ProfileConnection.REQUEST_DENY:
            connection.state = models.ProfileConnection.STATE_INACTIVE
            connection.save()

            # inactivate
            models.ProfileConnection.objects.filter(
                connector=request.user.profile, # one that requested
                connectee__slug=slug,
                status=models.ProfileConnection.STATUS_PENDING,
                state=models.ProfileConnection.STATE_ACTIVE
            ).update(
                state=models.ProfileConnection.STATE_INACTIVE,
                updated_at=timezone.now()
            )

        return True


class AccountsConnectionsRequestDenyForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        now = timezone.now()

        if slug == request.user.profile.slug:
            raise ValidationError('10035')

        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        # inactivate any from request side
        models.ProfileConnection.objects.filter(
                connector=request.user.profile, # one that requested
                connectee__slug=slug,
                state=models.ProfileConnection.STATE_ACTIVE
        ).update(
            state=models.ProfileConnection.STATE_INACTIVE,
            updated_at=now
        )
        return True


class AccountsConnectionsAcceptedForm(BaseStaticForm):
    serializer_class = serializers.ConnectionSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):

        qs = None
        slug = kwargs.get('slug', None)
        try:
            return models.ProfileConnection.objects.filter(
                    Q(Q(connectee__slug=slug)|Q(connector__slug=slug)) \
                    & Q(status=models.ProfileConnection.STATUS_ACCEPTED)
                    & Q(state=models.ProfileConnection.STATE_ACTIVE)
                ).annotate(user_slug=Value(slug, output_field=CharField()))
        except Exception as e:
            return models.ProfileConnection.objects.none()


class AccountsConnectionsPendingForm(BaseStaticForm):
    serializer_class = serializers.ConnectionSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):

        return models.ProfileConnection.objects.filter(
            Q(connectee=request.user.profile) \
            & Q(status=models.ProfileConnection.STATUS_PENDING)
            & Q(state=models.ProfileConnection.STATE_ACTIVE)
        ).annotate(user_slug=Value(request.user.profile.slug, output_field=CharField()))



class AccountsConnectionsRequestsForm(BaseStaticForm):
    serializer_class = serializers.ConnectionSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):

        qs = models.ProfileConnection.objects.filter(
                connector=request.user.profile,
                status=models.ProfileConnection.STATUS_PENDING,
                state=models.ProfileConnection.STATE_ACTIVE
        ).annotate(user_slug=Value(request.user.profile.slug, output_field=CharField()))
        return qs



class AccountsProfileReportForm(forms.Form):
    slug = forms.CharField()
    reason = forms.CharField()
    description = forms.CharField(required=False)

    def handle(self, view, request, *args, **kwargs):
        slug = self.cleaned_data.get('slug')
        profile = None

        if slug == request.user.profile.slug:
            raise ValidationError('10036')

        try:
            profile = models.Profile.people.state_active().get(slug=slug)
        except:
            raise ValidationError('10011')

        models.ProfileReport.objects.create(
            reported_to=profile,
            reason=self.cleaned_data.get('reason'),
            description=self.cleaned_data.get('description'),
            reported_by=request.user.profile
        )

        return True


# Useful
class AccountsProfileSearchForm(BaseStaticForm):
    serializer_class = serializers.ProfileSearchSerializer
    page_counter = -1

    list_filter = [
        'user__groups__name__in',
        'is_certified',
    ]

    search_fields = [
        'slug',
        'fullname',
        'bio',
        'about',
        'user__username',
        'user__groups__name',
        'tags__text',
        'website',
        'location',
    ]

    def _final_out(self, serialize_out, view, request, *args, **kwargs):
        serialized = super()._final_out(serialize_out)

        models.Activity.objects.create(
            type=models.Activity.TYPE_PROFILE_SEARCH,
            params_json=json.dumps(self.cleaned_data, cls=ModelEncoder),
            response_json=json.dumps(serialized, cls=ModelEncoder),
            created_by=request.user.profile if not request.user.is_anonymous else None
        )
        return serialized

    def get_queryset(self, view, request, *args, **kwargs):
        return models.Profile.people.state_active().common_groups()


class AccountsOrganizerDocumentsForm(BaseStaticForm):
    serializer_class = serializers.DocumentSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):
        return models.Document.objects.filter(
                created_by=request.user.profile,
                state=models.DocumentType.STATE_ACTIVE
            )


class AccountsOrganizerDocumentAddForm(forms.Form):
    type = forms.CharField()
    file = forms.FileField()
    description = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data

        type, c = models.DocumentType.objects.get_or_create(text=data['type'])
        data['created_by'] = request.user.profile
        doc = models.Document.objects.create(**data)

        return serializers.DocumentSerializer(doc).data


class AccountsOrganizerDocumentRemoveForm(forms.Form):
    slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        try:
            models.Document.objects.filter(
                slug=data['slug'],
                created_by=request.user.profile).delete()
        except: return True
        return True


class StaticDocumentTypeForm(BaseStaticForm):
    serializer_class = serializers.DocumentTypeSerializer
    page_counter = -1

    search_fields = [
        'text'
    ]

    def get_queryset(self, view, request, *args, **kwargs):
        return models.DocumentType.objects.filter(
                state=models.DocumentType.STATE_ACTIVE
            )


# messages

class ChatRoomsForm(BaseStaticForm):
    """all available convo rooms related to user"""

    serializer_class = serializers.ChatRoomSerializer
    page_counter = -1

    search_fields = [
        'members__fullname',
        'members__user__username',
        'title'
    ]

    def get_queryset(self, view, request, *args, **kwargs):
        return models.ChatRoom.objects.filter(
                members__in=[request.user.profile],
                state=models.ChatRoom.STATE_ACTIVE
            ).annotate(
                profile=Value(request.user.profile.slug, output_field=CharField())
            )


class ChatRoomGetForm(forms.Form):
    slug = forms.CharField(required=False) # chatroom
    user_slugs = base_fields.ArrayField(required=False)

    def handle(self, view, request, *args, **kwargs):
        user_slugs = self.cleaned_data['user_slugs']
        slug = self.cleaned_data['slug']

        chatroom = None
        if slug:
            try: chatroom = models.ChatRoom.objects.get(
                slug=slug, members__in=[request.user.profile])
            except: raise ValidationError('10038')
            chatroom.profile = request.user.profile
        # check validity use for new convo
        elif user_slugs:
            # if request.user.profile.slug in user_slugs:
            #     raise ValidationError('10040')

            user_slugs.append(request.user.profile)
            try:
                user_slugs = list(set(
                    map(lambda user: models.Profile.people.state_active(
                        ).get(slug=user), user_slugs)))
            except Exception as e:
                raise ValidationError('10039')

            # group convo
            if len(user_slugs) > 2:
                chatroom = models.ChatRoom.objects.create(
                    type=models.ChatRoom.TYPE_GROUP)
                for user in user_slugs: chatroom.members.add(user)
            else: # 2 or 1

                chatroom = models.ChatRoom.objects.filter(
                    members__in=user_slugs
                ).annotate(num_counts=Count('members')
                ).filter(Q(num_counts=len(user_slugs)))

                for user in user_slugs:
                    chatroom=chatroom.filter(members__in=[user])

                if chatroom.exists(): chatroom = chatroom.first()
                else:
                    chatroom = models.ChatRoom.objects.create()
                    for user in user_slugs: chatroom.members.add(user)
            chatroom.profile = request.user.profile.slug
        else: raise ValidationError('10041')
        return serializers.ChatRoomSerializer(chatroom).data


class ChatMessagesForm(BaseStaticForm):
    serializer_class = serializers.MessageSerializer
    page_counter = -1


    list_filter = [
         # unread , also can be used whenever there is a refresh happening
        'chatroom__slug',
    ]

    def custom_filter(self, key, val):
        if key and key == 'is_readed':
            return ~Q(seen_by__in=bool(val))
        return None

    def get_queryset(self, view, request, *args, **kwargs):
        qs =  models.Message.objects.filter(
            chatroom__members__in=[request.user.profile,]
        ).annotate(
            is_readed=ExpressionWrapper(
                Q(seen_by__in=[request.user.profile]),
                output_field=BooleanField())
        ).order_by('created_at')

        return qs


class ChatMessageAddForm(forms.Form):
    slug = forms.CharField()
    text = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        data = self.cleaned_data
        data['created_by'] = request.user.profile

        try:
            chatroom = models.ChatRoom.objects.get(
                slug=data.pop('slug'),state=models.ChatRoom.STATE_ACTIVE)
        except: raise ValidationError('10038')

        data['chatroom'] = chatroom
        message = models.Message.objects.create(**data)
        message.seen_by.add(data['created_by'])
        message.is_readed = True
        return serializers.MessageSerializer(message).data


class ChatMessageRemoveForm(forms.Form):
    slug = forms.CharField()
    chatroom_slug = forms.CharField()

    def handle(self, view, request, *args, **kwargs):
        now = timezone.now()
        models.Message.objects.filter(
            slug=self.cleaned_data['slug'],
            chatroom__slug=self.cleaned_data['chatroom_slug'],
            created_by=request.user.profile
        ).update(state=models.Message.STATE_INACTIVE, updated_at=now)
        return True


class ChatMessagesUnreadUpdateForm(forms.Form):
    slugs = base_fields.ArrayField(required=False)

    def handle(self, view, request, *args, **kwargs):
        now = timezone.now()

        m = models.Message.objects.none()

        if self.cleaned_data['slugs']:
            for m in models.Message.objects.filter(
                slug__in=self.cleaned_data['slugs'],
            ).exclude(seen_by__in=[request.user.profile]
            ):
                m.seen_by.add(request.user.profile)
                m.save()
                m.is_readed = True

        return serializers.MessageSerializer(m, many=True).data


# websocket others

# notif

class NotificationsForm(BaseStaticForm):
    serializer_class = serializers.NotificationSerializer
    page_counter = -1

    list_filter = [
        'is_readed'
    ]

    order_list = [
        'created_at'
    ]

    def get_queryset(self, view, request, *args, **kwargs):
        return models.Notification.objects.filter(
            notified_to=request.user.profile
        )


class NotificationsUpdateForm(forms.Form):
    # slugs = base_fields.ArrayField()

    def handle(self, view, request, *args, **kwargs):
        now = timezone.now()

        n = models.Notification.objects.filter(
            notified_to=request.user.profile,
            is_readed=False,
            created_at__lte=now + timezone.timedelta(seconds=120))
        m = []
        for _n in n:
            _n.is_readed=True
            _n.save()
            m.append(_n)

        return serializers.NotificationSerializer(m, many=True).data


# activity logs

# reco


from apps.account.recommendation import recommend


class RecommendServicesForm(BaseStaticForm):
    serializer_class = serializers.Userv2WithProfileSerializer
    page_counter = -1

    list_filter = [
        'user__groups__name__in',
        'is_certified',
    ]

    search_fields = [
        'slug',
        'fullname',
        'bio',
        'about',
        'user__username',
        'user__groups__name',
        'tags__text',
        'website',
        'location',
    ]

    def custom_count(self, qs):
        return len(qs)

    def get_queryset(self, view, request, *args, **kwargs):
        A = recommend.Aggregation(request.user.profile)
        R = recommend.Recommendation(A, request)

        try:
            return R.content_recommend(type='services')
        except Exception as e:
            raise Exception(e)


        # try:
        # except Exception as e:
        #     raise Exception(e)
        #     return R.err_recommend(type='services').exclude(
        #     slug=request.user.profile)


class RecommendEmptyForm(BaseStaticForm):
    serializer_class = serializers.Userv2WithProfileSerializer
    page_counter = -1

    def custom_count(self, qs):
        return len(qs)

    def get_queryset(self, view, request, *args, **kwargs):
        A = recommend.Aggregation(request.user.profile)
        R = recommend.Recommendation(A, request)

        try:
            return R.content_recommend(type='services')
        except Exception as e:
            raise Exception(e)

class TopTagsForm(BaseStaticForm):

    serializer_class = serializers.TagSerializer
    page_counter = -1

    def get_queryset(self, view, request, *args, **kwargs):
        return recommend.top_tags()