import datetime
import importlib
import json
from django.contrib.auth import get_user_model
from django.conf import settings as django_settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils import timezone

from .exceptions import InvalidTokenError


User = get_user_model()


class SourceToken(models.Model):
    STATE_ACTIVE = 'ACTIVE'
    STATE_INACTIVE = 'INACTIVE'

    # static
    ACTION_REGISTRATION_OTP = 'registration-otp'
    ACTION_CHANGE_PASSWORD_OTP = 'change-password-otp'
    ACTION_CONFIRM_APPLICATION_OTP = 'confirm-application-otp'

    APPLICATION_SECURITY_TOKEN_LENGTH = 30
    EMAIL_SECURITY_TOKEN_LENGTH = 30

    action = models.CharField(max_length=50, null=True, blank=True)
    code = models.CharField(max_length=50, null=True, blank=True)
    created_by = models.ForeignKey(django_settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    settings_json = models.TextField(null=True, blank=True)
    expired_at = models.DateTimeField(null=True, blank=True)
    is_used = models.BooleanField(default=False, null=True, blank=True)
    state = models.CharField(max_length=50, default=STATE_ACTIVE, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

    @property
    def settings(self):
        return json.loads(self.settings_json or '{}')

    @staticmethod
    def generate_key(length=30):
        method = 'oauthlib.common.generate_token'
        module = importlib.import_module('.'.join(method.split('.')[0:-1]))
        func = getattr(module, method.split('.')[-1])

        return func(length)

    @classmethod
    def create_token(cls, action, user=None, length=30, settings=None, expiration=0):
        key = cls.generate_key(length)
        token = cls._default_manager.create(
            action=action,
            code=key,
            created_by=user,
            settings_json=json.dumps(settings),
            expired_at=timezone.now() \
             + timezone.timedelta(seconds=expiration or django_settings.OTP_EXPIRATION_SECONDS)
        )

        #just return the code
        return token.code

    @classmethod
    def verify_token(cls, action, code, is_expire=True, *args, **kwargs):

        try:

            if django_settings.OTP_EXPIRATION_SECONDS != -1:
                kwargs['expired_at__gte'] = timezone.now()

            source = cls._default_manager.get(
                action=action,
                code=code,
                is_used=False,
                state=cls.STATE_ACTIVE,
                **kwargs
            )
        except cls.DoesNotExist:
            raise InvalidTokenError('Invalid token : Does Not Exists. Expired. Used.')

        if is_expire:
            source.is_used = True
            source.save()

        return source.settings


