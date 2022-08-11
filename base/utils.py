import logging
import re
import requests

from django.conf import settings
from django.core.mail import EmailMessage


logger = logging.getLogger(__name__)


def send_mail(sender, recipients, subject, body, return_first=False):
    """
    Function base sending email
    defaults to html type file
    @param sender (str) - sender
    @param recipient list of (str) - receivers
    @param subject (str) - header
    @param body (str) - context
    @param return_first - return the email instance.
    """
    email_message = EmailMessage(subject, body, sender, recipients)
    email_message.content_subtype = 'html'

    if return_first:
        return email_message

    # this should be try except.
    email_message.send()
    logger.info("Mail sent.")



def verify_captcha_api(request):
    """
    Verify captcha via Google Recaptcha v3 API version
    """
    verify_site = r"https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': settings.GOOGLE_SECRET_KEY,
        'response': request.data.get('g-recaptcha-response'),
        'remoteip': request.META.get('REMOTE_ADDR')
    }

    r = requests.post(verify_site, data=data)

    result = r.json()

    if not result['success']:
        logger.exception("+".join(result['error-codes']))

    # api returns success true|false
    return result['success']


def upperize_string(string=""):
    """Upperize string"""
    return string.upper()


def sanitize_string(string="", regex=r"[^a-zA-Z0-9]+", func=upperize_string):
    """Removes characters based on regex and can modify string before subbing.
       @param string (str)
       @param regex - default to /W
       @param func - function to modify string first def. upperize
       @out (str)
    """

    return " ".join(
        map(
            lambda s: re.sub(regex, '', func(s)), string.split()
        ))


from ipware import get_client_ip
from django.contrib.gis.geoip2 import GeoIP2
from geopy import distance


def get_ip(request):
    client_ip, is_routable = get_client_ip(request)
    return client_ip


def get_lat_long(request, func=get_ip, flip=False):

    ip = request
    try:
        ip = func(request)
    except:
        ip = request

    geo = GeoIP2()

    if settings.DEBUG and not flip:
        return geo.lat_lon(settings.GEO_DEBUG_IP)

    return geo.lat_lon(ip)



def get_geo_address(request, func=get_ip, flip=False):

    ip = request
    try:
        ip = func(request)
    except:
        ip = request

    geo = GeoIP2()

    address_dict = None
    if settings.DEBUG and not flip:
        address_dict =  geo.city(settings.GEO_DEBUG_IP)
    else:
        address_dict = geo.city(ip)

    return "{city}, {country}, {continent}".format(
            city=address_dict['city'],
            country=address_dict['country_name'],
            continent=address_dict['continent_name']
        )



def get_distance(dis1, dis2):
    return distance.distance(dis1, dis2).miles