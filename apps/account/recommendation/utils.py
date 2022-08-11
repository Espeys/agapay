PROFILE_SEARCH = '/api/v1/accounts/profile/search/'
NEWSFEED_SEARCH = '/api/v1/posts/newsfeed/'

ACTIVITY_PATHS = [
    '/api/v1/accounts/profile/search/',
    '/accounts/profile/follow/',
    '/api/v1/accounts/connection/request/',
    '/api/v1/accounts/connection/status/',
    '/api/v1/posts/newsfeed/',
    '/api/v1/posts/share/',
    '/api/v1/posts/bookmark/'
    '/api/v1/posts/like/',
    '/api/v1/posts/comment/add/',
    '/api/v1/accounts/profile/',
    '/api/v1/accounts/profile/update/',
]

SEARCH_PATHS = [
    '/api/v1/accounts/profile/search/',
    '/api/v1/posts/newsfeed/',
]


from apps.account.models import Profile
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.conf import settings
import pandas as pd

import os

# generate users

User = get_user_model()


DUMMY_PATH = os.path.join(settings.BASE_DIR, 'dummy')
DUMMY_FILE = 'retweeted_user_reserved.csv'

# password = User.objects.make_random_password()

def create_users():
    user_df = pd.read_csv(DUMMY_PATH+'/'+DUMMY_FILE)

    # generate
    for index, row in user_df.head(300).iterrows():
        user = User.objects.create(
                username=row['screen_name']+'@gmail.com',
                email=row['screen_name']+'@gmail.com',
                first_name=row['name'],
                last_name=''
            )
        user.profile.fullname=user.first_name+user.last_name
        user.profile.about = row['description']
        user.profile.save()

        group,c  = Group.objects.get_or_create(name=Profile.GROUP_ORGANIZER)

        user.groups.add(group)
        password = User.objects.make_random_password()
        user.set_password(password)
        user.save()