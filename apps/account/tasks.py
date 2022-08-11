import json
from celery import shared_task
from celery.decorators import task
from celery.utils.log import get_task_logger
from config.celery import app


logger = get_task_logger(__name__)


@app.task
def async_cleartokens(*args):
    from django.core.management import call_command

    logger.info('Clear tokens.')
    call_command('cleartokens')

    return True

# add clear unverified email

@app.task
def async_clear_unverify_accounts(*args):
    from .models import Profile

    logger.info('Clear accounts')
    Profile.objects.filter(
        is_verified=False,
        user__is_staff=False
    ).delete()

    return True