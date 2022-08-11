from django import forms
from django.core.exceptions import ValidationError
from django.urls import path
from django.utils import timezone

from .errors import ERRORS_DICT
from .views import GenericView

from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2


class PingForm(forms.Form):
    error = forms.BooleanField(initial=False, required=False)

    def handle(self, view, request, *args, **kwargs):

        client_ip, is_routable = get_client_ip(
            request)

        g = GeoIP2()
        x = g.city(client_ip)

        data = self.cleaned_data
        error = data.get('error')

        if error:
            raise ValidationError('1')
        return timezone.localtime(timezone.now())


class PingView(GenericView):
    form_class = PingForm
    errors_dict = ERRORS_DICT

    def post(self, *args, **kwargs):
        return self.process(*args, **kwargs)


urlpatterns = [
    path('ping/', PingView.as_view(), name='ping'),
]
