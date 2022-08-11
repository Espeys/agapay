import json
import phonenumbers
from django.conf import settings
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms.fields import (
        CharField,
        ImageField,
        FileField,
    )
from django.forms.widgets import TextInput, Textarea
from django.utils.translation import gettext_lazy as _, ngettext_lazy


class UpperCharField(CharField):
    """Auto upper values"""

    def clean(self, value):
        value = super().clean(value)

        if value:
            return value.upper()
        return value


class MobileNumberField(CharField):
    """
    Customized charfield caters mobile numbers and output a standard one.
    """

    defaut_error_messages = {
        'invalid': _("Invalid format. %(error)s"),
        'invalid_length': _("Not equal to required digits. %(digits)d"),
    }

    def __init__(self, region=settings.DEFAULT_MOBILE_REGION, length=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.region = region
        self.length = length

        for key, val in self.defaut_error_messages.items():
            check_key = self.error_messages.get(key, None)

            if not check_key:
                self.error_messages[key] = val

    def clean(self, value):
        # run normal charfield clean - to_python and validate
        # return values
        phone_number = super().clean(value)

        if phone_number:

            phone_number = "".join(phone_number.split())

            if self.length and len(phone_number) != self.length:
                raise ValidationError(_(self.error_messages['invalid_length']),
                    code='invalid_length',
                    params={'digits': self.length}
                )

            try:
                phone_number = phonenumbers.parse(
                    phone_number,
                    self.region
                )
            except Exception as e:
                raise ValidationError(_(self.error_messages['invalid']),
                    code='invalid',
                    params={'error': e}
            )

            # since only need +63....
            phone_number = phonenumbers.format_number(
                phone_number,
                phonenumbers.PhoneNumberFormat.E164
            )

        return phone_number


class JSONField(CharField):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self, value):
        value = super().clean(value)

        if value in self.empty_values:
            return value

        if not isinstance(value, (str, bytes)):
            return value

        try:
            return json.loads(value)
        except json.JSONDecodeError:
            raise ValidationError('Cannot translate')


class TypedJSONField(JSONField):

    defaut_error_messages = {
        'invalid_type': _('Type of input not matching specified type.')
    }

    def __init__(self, type=None, *args, **kwargs):
        self.type = type
        super().__init__(*args, **kwargs)

        for key, val in self.defaut_error_messages.items():
            check_key = self.error_messages.get(key, None)

            if not check_key:
                self.error_messages[key] = val

    def clean(self, value):

        value = super().clean(value)

        if self.required or value:

            if not isinstance(self.type, (list, tuple)):
                self.type = [self.type]

            # expecting a converted one
            if type(value) not in self.type:
                raise ValidationError(self.error_messages['invalid_type'])

        return value

class ArrayField(TypedJSONField):

    default_error_messages = {
        'invalid_value_type': _('Value(s) type of input not matching specified type.')
    }

    def __init__(self, value_type=str, *args, **kwargs):
        self.value_type = value_type
        super().__init__(type=list, *args, **kwargs)

        for key, val in self.defaut_error_messages.items():
            check_key = self.error_messages.get(key, None)

            if not check_key:
                self.error_messages[key] = val

    def clean(self, value):
        value = super().clean(value)

        if value:
            if not all(map(lambda val: type(val)==self.value_type, value)):
                raise ValidationError(self.error_messages['invalid_value_type'])

        return value


class ContentRestrictedImageField(ImageField):

    defaut_error_messages = {
        'invalid_extension': _("File was not on the list of [%(extensions)s.]"),
        'invalid_max_size': _("Maximum file size is %(size)d byte(s)"),
        'invalid_min_height': _("Minimum height exceeded %(height)d"),
        'invalid_max_height': _("Maximum height exceeded %(height)d"),
        'invalid_min_width': _("Minimum width exceeded %(width)d"),
        'invalid_max_width': _("Maximum width exceeded %(width)d"),
    }

    def __init__(self, *args, **kwargs):

        self.accepted_extensions = kwargs.pop('accepted_extensions', None)
        if self.accepted_extensions and (not isinstance(self.accepted_extensions, (list, tuple))):
            self.accepted_extensions = list(self.accepted_extensions)

        self.max_size = kwargs.pop('max_size', None)
        if self.max_size:
            self.max_size = self.max_size * 1024 * 1024

        self.min_width = kwargs.pop('min_width', None)
        self.min_height = kwargs.pop('min_height', None)

        self.max_width = kwargs.pop('max_width', None)
        self.max_height = kwargs.pop('max_height', None)

        super().__init__(*args, **kwargs)

        for key, val in self.defaut_error_messages.items():
            check_key = self.error_messages.get(key, None)

            if not check_key:
                self.error_messages[key] = val

    def clean(self, *args, **kwargs):
        # yes dont care about the other data here
        file = super().clean(*args, **kwargs)
        # return None if self.required = False but no file attach
        if file is None:
            return None

        # else validate it
        # check if there is accepted_extensions to do
        if self.accepted_extensions:
            # there is, check it in the list or tuple
            ext = file.image.format
            if ext not in self.accepted_extensions:
                extension = ','.join(self.accepted_extensions)
                params = {'extensions': extension}
                raise ValidationError(_(self.error_messages['invalid_extension']),
                    code='invalid_extension',
                    params=params)

        if (self.max_size is not None) and (file.size > self.max_size):
            raise ValidationError(_(self.error_messages['invalid_max_size']),
                code='invalid_max_size',
                params={'size': self.max_size})

        height = file.image.height
        if (self.min_height is not None) and (height > self.min_height):
            raise ValidationError(_(self.error_messages['invalid_min_height']),
                code='invalid_min_height',
                params={'height': self.min_height})

        if (self.max_height is not None) and (height > self.max_height):
            raise ValidationError(_(self.error_messages['invalid_max_height']),
                code='invalid_max_height',
                params={'height': self.max_height})

        width = file.image.width
        if (self.min_width is not None) and (width > self.min_width):
            raise ValidationError(_(self.error_messages['invalid_min_width']),
                code='invalid_min_width',
                params={'width': self.min_width})

        if (self.max_width is not None) and (width > self.max_width):
            raise ValidationError(_(self.error_messages['invalid_max_width']),
                code='invalid_max_width',
                params={'width': self.max_width})

        return file


class ContentRestrictedFileField(FileField):

    defaut_error_messages = {
        'invalid_types': _("File was not accepted on the list of [%(types)s] ."),
        'invalid_extension': _("File had not a valid extensions on the list of [%(extensions)s]."),
        'invalid_max_size': _("Maximum file size is %(size)d byte(s)."),
    }

    def __init__(self, *args, **kwargs):

        self.accepted_extensions = kwargs.pop('accepted_extensions', None)
        if self.accepted_extensions and (not isinstance(self.accepted_extensions, (list, tuple))):
            self.accepted_extensions = list(self.accepted_extensions)

        self.accepted_types = kwargs.pop('accepted_types', None)
        if self.accepted_types and (not isinstance(self.accepted_types, (list, tuple))):
            self.accepted_types = list(self.accepted_types)

        self.max_size = kwargs.pop('max_size', None)
        if self.max_size:
            self.max_size = self.max_size * 1024 * 1024

        super().__init__(*args, **kwargs)

        for key, val in self.defaut_error_messages.items():
            check_key = self.error_messages.get(key, None)

            if not check_key:
                self.error_messages[key] = val

    def clean(self, *args, **kwargs):

        file = super().clean(*args, **kwargs)

        if file is None:
            return None

        # validate now
        # check max_size
        if (self.max_size is not None) and file.size > self.max_size:
            raise ValidationError(_(self.error_messages['invalid_max_size']),
                code='invalid_max_size',
                params={'size': self.max_size})

        if not (self.accepted_types or self.accepted_extensions):
            return file

        # NOTE ALWAYS DOUBLE VALIDATE HERE FOR BETTER PROTECTION
        # DO MAGIC TO GET THE REAL TYPE AND DO EXTENSION VALIDATIONS
        import os
        import magic

        file_type = magic.from_buffer(file.read(), mime=True)
        ext = os.path.splitext(file.name)[1]

        if self.accepted_types and (file_type not in self.accepted_types):
            types = ', '.join(t.replace('/', '.') for t in self.accepted_types)
            params = {'types': types}

            raise ValidationError(_(self.error_messages['invalid_types']),
                code='invalid_types',
                params=params)

        if self.accepted_extensions and (ext not in self.accepted_extensions):
            extension = ','.join(self.accepted_extensions)
            params = {'extensions': extension}

            raise ValidationError(_(self.error_messages['invalid_extension']),
                code='invalid_extension',
                params=params)

        return file




