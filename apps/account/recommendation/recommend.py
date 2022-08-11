from . import models, utils

from apps.account import models as account_models
from apps.account import serializers as account_serializers
from apps.post import models as post_models
from apps.post import serializers as post_serializers
from rest_framework_tracking.models import APIRequestLog

from django.db.models import (
        Count, Q, F, Value, IntegerField,
        CharField, Case, When, TextField, FloatField
)
from django.db.models.functions import Concat
from django.db.models.expressions import Window
from django.db.models.functions import RowNumber

from base import utils as base_utils
from base.encoders import ModelEncoder, ModelDecoder
import json

import ast

from django.utils import timezone

import pandas as pd
import numpy as np
from ast import literal_eval
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet



class Aggregation:

    def __init__(self, user):
        self.user = user
        self.searches = []
        self.tags = []

        self.aggregate_tags()

    def aggregate_tags(self, *args, **kwargs):

        # tags and searches
        # following = account_models.ProfileFollower.objects.filter(
        #     follower=self.user
        # ).values_list('follower_id', flat=True)
        # connectee = account_models.ProfileConnection.objects.filter(
        #     connectee=self.user
        # ).values_list('connector_id', flat=True)
        # connector = account_models.ProfileConnection.objects.filter(
        #     connector=self.user
        # ).values_list('connectee_id', flat=True)

        now = timezone.now()


        # searches from activities
        activities = account_models.Activity.objects.filter(
            created_by=self.user
        )

        # try first if there immediate activity that is not search within the day
        # and the latest e.g share, like, comment, follow, connect request,
        # if it is posts then segregate to post slug?

        self.instant_activity = activities.filter(created_at__date=now
            ).order_by('-created_at').first() # any types

        # just a backup and useful since its already aggregated
        for activity in activities.filter(type__in=[
                account_models.Activity.TYPE_PROFILE_SEARCH,
                account_models.Activity.TYPE_NEWSFEED_SEARCH
            ]):
            # raise Exception(json.loads(activity.params_json))
            params = json.loads(activity.params_json)
            self.searches.extend(params['q'].split(' ')) # should have a spliiter
            # response = json.loads(activity.response_json)
        self.all_tags = [str(txt) for txt in self.user.tags.all().values_list('text', flat=True)]
        self.searches.extend(self.all_tags) # extend those


        # remove this due to the fact that this is aggregrating all
        #     if activity.type in [
        #         account_models.Activity.TYPE_PROFILE_SEARCH,
        #         account_models.Activity.TYPE_NEWSFEED_SEARCH]:
        #         if hasattr(response, 'items'): # list
        #             for item in response['items']:
        #                 self.tags.extend(item.get('tags', []))
        #         else: self.tags.extend(response.get('tags',[]))
        # self.tags = list(set(map(lambda d: d, self.tags)))

        # self.all_tags = post_models.PostTag.objects.filter(
        #     Q(postitem__created_by=self.user) \
        #     | Q(postitem__created_by__in=following) \
        #     | Q(postitem__created_by__in=connectee) \
        #     | Q(postitem__created_by__in=connector) \
        #     | Q(profile__in=connectee) \
        #     | Q(profile__in=connector) \
        #     | Q(profile__in=following) \
        #     | Q(profile=self.user) \
        #     # | Q(text__in=self.tags)
        # ).annotate(num_counts=Count('postitem__tags')+Count('profile__tags'))
        # your tags if have
        # self.all_tags
        # raise Exception(self.all_tags.first().t)

    def aggregate_to_db(self):
        pass


class Recommendation:
    """recommend user with something"""

    post_search_fields = [
        'description',
        'email',
        'weblink',
        'created_by__user__username',
        'created_by__fullname',
        'tags__text',
        'item_type',
        'promotion_type',
    ]

    user_search_fields = [
        'slug',
        'fullname',
        'user__username',
        'user__groups__name',
        'tags__text',
        'website',
        'location',
        'bio',
        'about',
    ]

    def __init__(self, aggregator, request, *args, **kwargs):
        self.aggregator = aggregator
        self.request = request

    def process_query(self, key, item):
        """
        Validate key if contains not string keywords e.g gte, lte, isnull
        didnt try in range but base on example range takes 2 keywords...
        else do __icontains as default.
        it should be expr = ''
        """
        # will add more
        if key.endswith(
            (
                '__gte',
                '__lte',
                '__isnull',
                '__iexact',
                '__exact',
                '__lt',
            )):
            return {key:item}

        # use the default
        # in order to use the exact use __exact
        return {'{}__icontains'.format(key): item}

    def _build_q_search(self, type='promotion'):
        search_fields = self.post_search_fields if type=='promotion' \
             else self.user_search_fields
        data_q = list(filter(None,set(self.aggregator.searches)))

        filters = Q()
        for i in search_fields:
            for q in data_q:
                filters |= Q(**self.process_query(i, q))
        return filters

    def _build_qs_data_search(self, type='promotion', qs=[]):
        search_fields = self.post_search_fields if type=='promotion' \
             else self.user_search_fields
        data_q = qs

        filters = Q()
        for i in search_fields:
            for q in data_q:
                filters |= Q(**self.process_query(i, q))
        return filters

    def _build_tag_search(self, type):
        search_fields = self.post_search_fields if type=='promotion' \
             else self.user_search_fields

        tag_fields = ['tags__text']
        data_q = self.aggregator.all_tags
        filters = Q()

        for i in tag_fields:
            for t in data_q:
                filters |= Q(**self.process_query(i, t))
        return filters

    def random_recommend(self, type='promotion', length=10, *args, **kwargs):
        if type == 'promotion':
            posts = post_models.PostItem.objects.filter(
                    item_type=post_models.PostItem.ITEM_TYPE_PROMOTION,
                    state=post_models.PostItem.STATE_ACTIVE,
                ).annotate(
                    miles=Value(0, output_field=FloatField()),
                    request=Value(self.aggregator.user.slug, output_field=CharField())
                ).order_by('?')
            return posts
        if type == 'services':
            services = account_models.Profile.people.filter(
                user__groups__name__in=[
                    account_models.Profile.GROUP_ORGANIZER,
                    account_models.Profile.GROUP_INDIVIDUAL
                ],
                state=account_models.Profile.STATE_ACTIVE
            ).order_by('?')
            return services
        raise Exception('No specified')

    def simple_recommend(self, type='promotion', length=10, *args, **kwargs):
        if not self.aggregator: raise Exception('Put an aggregator')

        build_search = self._build_q_search(type=type)
        build_tag = self._build_tag_search(type=type)

        if type == 'promotion':
            posts = post_models.PostItem.objects.filter(
                    item_type=post_models.PostItem.ITEM_TYPE_PROMOTION,
                    state=post_models.PostItem.STATE_ACTIVE
            ).annotate(
                miles=Value(0, output_field=FloatField()),
                request=Value(self.aggregator.user.slug, output_field=CharField())
            )
            posts = posts.filter(Q(build_search) | Q(build_tag))
            return posts

        if type == 'services':
            services = account_models.Profile.people.filter(
                user__groups__name__in=[
                    account_models.Profile.GROUP_ORGANIZER,
                    account_models.Profile.GROUP_INDIVIDUAL
                ],
                state=account_models.Profile.STATE_ACTIVE
            )
            services = services.filter(Q(build_search) | Q(build_tag))
            return services
        raise Exception('No specified')

    def err_recommend(self, type='promotion', length=10, *args, **kwargs):
        if not self.aggregator: raise Exception('Put an aggregator')

        build_search = self._build_q_search(type='promotion')
        build_tag = self._build_tag_search(type='promotion')

        posts = post_models.PostItem.objects.filter(
                item_type=post_models.PostItem.ITEM_TYPE_PROMOTION,
                state=post_models.PostItem.STATE_ACTIVE
        ).annotate(
            likers_count=Count('likes'),
            commenters_count=Count('postcomment__post'),
            sharers_count=Count('shared_post'),
            followers_count=Count('created_by__following') + 1
        )
        if not posts and type=='promotion': return posts.none()
        if not posts and type=='services': return account_models.Profile.people.none()

        posts_len = posts.count()
        posts = posts.annotate(
            weight_rating = Case(
                When(followers_count=0, then=0),
                default= ( F('likers_count') \
                    + F('commenters_count') \
                    + F('sharers_count') ) / F('followers_count')),
            miles=Value(0, output_field=FloatField()),
            request=Value(self.aggregator.user.slug, output_field=CharField())
        )
        # anything
        posts = posts.filter(
            Q(build_search) | Q(build_tag)
        ).order_by('-weight_rating')

        if type == 'promotion': return posts
        if type == 'services':
            users = posts.values_list('created_by__id', flat=True)
            return account_models.Profile.people.state_active().filter(
                user__groups__name__in=[account_models.Profile.GROUP_ORGANIZER,
                account_models.Profile.GROUP_INDIVIDUAL],
                state=account_models.Profile.STATE_ACTIVE,
                user__in=users)
        raise Exception('No specified')

    def content_recommend(self, type='promotion', length=10, *args, **kwargs):
        if not self.aggregator: raise Exception('Put an aggregator')

        build_search = self._build_q_search(type=type)
        # build_tag = self._build_tag_search(type=type)

        if type == 'promotion':

            posts = post_models.PostItem.objects.filter(
                item_type=post_models.PostItem.ITEM_TYPE_PROMOTION,
                state=post_models.PostItem.STATE_ACTIVE
            ).exclude(
                created_by__slug=self.aggregator.user
            ).annotate(
                likers_count=Count('likes'),
                commenters_count=Count('postcomment__post'),
                sharers_count=Count('shared_post'),
                followers_count=Count('created_by__following')
            )

            posts = posts.annotate(
                weight_rating = Case(
                    When(followers_count=0, then=0),
                    default= ( F('likers_count') \
                        + F('commenters_count') \
                        + F('sharers_count') ) / F('followers_count')
                )
            ).annotate(
                aggregated_description=Concat(
                    'description', Value(' '), 'created_by__fullname',
                    output_field=TextField())
            ).annotate(
                miles=Value(0, output_field=FloatField()),
                request=Value(self.aggregator.user.slug, output_field=CharField())
            )


            if not posts: return posts.none()


            targeted_post = None
            instant_activity = self.aggregator.instant_activity
            if instant_activity:
                response_json = json.loads(instant_activity.response_json)
                if instant_activity.type in [
                        account_models.Activity.TYPE_PROFILE_SEARCH,
                        account_models.Activity.TYPE_NEWSFEED_SEARCH
                    ]:
                    targeted_post = posts.filter(Q(build_search)).order_by('?').first()
                elif instant_activity.type in [
                        account_models.Activity.TYPE_FOLLOW,
                        account_models.Activity.TYPE_CONNECT_ACCEPT
                    ]:
                    targeted_post = posts.filter(created_by__slug=response_json.get('slug', '')
                        ).order_by('?').first()
                elif instant_activity.type == account_models.Activity.TYPE_CONNECT_REQUEST:
                    user = response_json['user']
                    targeted_post = posts.filter(created_by__slug=user.get('slug', '')
                        ).order_by('?').first()
                elif instant_activity.type in [
                    account_models.Activity.TYPE_POST_ADD,
                    account_models.Activity.TYPE_POST_COMMENT,
                    account_models.Activity.TYPE_POST_SUPPORT_ACCEPT
                ]:
                    targeted_post = posts.filter(slug=response_json['slug']).first()
                elif instant_activity.type == account_models.Activity.TYPE_POST_SHARE:
                    targeted_post = posts.filter(slug=response_json['shared_slug']).first()
                elif instant_activity.type == account_models.Activity.TYPE_POST_SUPPORT_REQUEST:
                    users = json.loads(instant_activity.params_json)['user_slugs']
                    users.append(response_json['created_by_slug'])
                    targeted_post = posts.filter(
                        created_by__slug__in=users).order_by('?').first()
                # randomize targeted posts
            else: targeted_post = posts.filter(Q(build_search)).order_by('?').first()

            if not targeted_post: return posts.none()

            # APPLY WEIGHTS
            # Concatenation
            posts_len = posts.count()

            ### description

            # tf = TfidfVectorizer(
            #     analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
            # tfidf_matrix = tf.fit_transform(
            #     posts.values_list('description', flat=True)
            # )
            # cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

            # # # range
            # indices = pd.Series(range(0, posts_len), index=posts.values_list('slug', flat=True))
            # indices_proxy = pd.Series(posts.values_list('slug', flat=True), index=range(0, posts_len))

            # idx = indices[targeted_post.slug]
            # sim_scores = list(enumerate(cosine_sim[idx]))
            # sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            # sim_scores = sim_scores[1:31]
            # post_indices = [i[0] for i in sim_scores]
            # post_proxy_indices = [indices_proxy[i] for i in post_indices]

            ### soup
            soup = []
            for post in posts: # ASSUMING THIS DOES NOT MESS UP WITH THE FILTER
                string = ' '.join(post.tags.values_list('text', flat=True)) \
                    + ' ' \
                    + ' '.join(post.created_by.fullname.split(' ')) \
                    + ' ' \
                    + ' '.join([post.item_type]) \
                    + ' ' \
                    + ' '.join(['' if not post.promotion_type else post.promotion_type]) \
                    + ' ' \
                    + ' '.join(['' if not post.help_type else post.help_type])
                post.soup = string
                soup.append(string)

            count = CountVectorizer(stop_words='english')
            count_matrix = count.fit_transform(soup)
            cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

            indices = pd.Series(range(0, posts_len),
                index=posts.values_list('slug', flat=True))
            indices_proxy = pd.Series(posts.values_list('slug', flat=True),
                index=range(0, posts_len))

            idx = indices[targeted_post.slug]
            sim_scores = list(enumerate(cosine_sim2[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:31] # idk what is this though it says top 30
            post_indices = [i[0] for i in sim_scores]
            post_proxy_indices = [indices_proxy[i] for i in post_indices]

            # posts = posts.filter(slug__in=post_proxy_indices
            #     )
            # .order_by(
            #     '-weight_rating'
            # )
            _iloc = []
            _iloc.append(targeted_post)
            for idx in post_proxy_indices:
                _iloc.append(posts.get(slug=idx))
            return _iloc

        if type == 'services':

            accounts = account_models.Profile.people.state_active().filter(
                user__groups__name__in=[
                account_models.Profile.GROUP_ORGANIZER,
                account_models.Profile.GROUP_INDIVIDUAL,
                # account_models.Profile.GROUP_CANDIDATE
                ],
                state=account_models.Profile.STATE_ACTIVE,
            ).exclude(slug=self.aggregator.user.slug)

            if not accounts: return accounts.none()
            accounts_len = accounts.count()

            # replaced this by activities from each week
            # then if there were a post or user interactions e.g like share comment follow connect
            # raise Exception(build_search)

            # query
            instant_activity = self.aggregator.instant_activity
            if instant_activity:
                response_json = json.loads(instant_activity.response_json)
                if instant_activity.type in [
                        account_models.Activity.TYPE_PROFILE_SEARCH,
                        account_models.Activity.TYPE_NEWSFEED_SEARCH
                    ]:
                    targeted_account = accounts.filter(Q(build_search)).order_by('?').first()
                elif instant_activity.type in [
                        account_models.Activity.TYPE_FOLLOW,
                        account_models.Activity.TYPE_CONNECT_ACCEPT
                    ]:
                    targeted_account = accounts.filter(slug=response_json.get('slug', '')).first()
                elif instant_activity.type == account_models.Activity.TYPE_CONNECT_REQUEST:
                    user = response_json['user']
                    targeted_account = accounts.filter(slug=user.get('slug', '')).first()
                elif instant_activity.type in [
                    account_models.Activity.TYPE_POST_COMMENT,
                    account_models.Activity.TYPE_POST_SUPPORT_ACCEPT
                ]:
                    targeted_account = accounts.filter(slug=response_json['created_by_slug']).first()
                elif instant_activity.type == account_models.Activity.TYPE_POST_ADD:
                    post = post_models.PostItem.objects.filter(slug=response_json['slug']).first()

                    _qs_search = self._build_qs_data_search(type='services', qs=post.tags.all().values_list('text', flat=True))
                    targeted_account = accounts.filter(Q(_qs_search)).order_by('?').first()
                    # raise Exception(targeted_account)
                    # targeted_account = accounts.filter(Q(build_search)).order_by('?').first()
                elif instant_activity.type == account_models.Activity.TYPE_POST_SHARE:
                    targeted_account = accounts.filter(slug=response_json['shared_created_by_slug']).first()
                elif instant_activity.type == account_models.Activity.TYPE_POST_SUPPORT_REQUEST:
                    users = json.loads(instant_activity.params_json)['user_slugs']
                    users.append(response_json['created_by_slug'])
                    targeted_account = accounts.filter(slug=users).first()
            else:
                targeted_account = accounts.filter(Q(build_search)).order_by('?').first()



            # raise Exception(build_search)
            # raise Exception(targeted_account.fullname)

            if not targeted_account: return accounts.none() # kekl

            soup = []
            for account in accounts: # ASSUMING THIS DOES NOT MESS UP WITH THE FILTER
                string = ' '.join(account.tags.values_list('text', flat=True)) \
                    + ' ' \
                    + ' '.join(account.fullname.split(' '))
                    # + ' ' \
                    # + ' '.join(['' if not account.bio else account.bio ]) \
                    # + ' ' \
                    # + ' '.join(['' if not account.about else account.about ])
                account.soup = string
                soup.append(string)

            count = CountVectorizer(stop_words='english')
            count_matrix = count.fit_transform(soup)
            cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

            indices = pd.Series(range(0, accounts_len),
                index=accounts.values_list('slug', flat=True))
            indices_proxy = pd.Series(accounts.values_list('slug', flat=True),
                index=range(0, accounts_len))

            idx = indices[targeted_account.slug]
            sim_scores = list(enumerate(cosine_sim2[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:31] # idk what is this though it says top 30
            accounts_indices = [i[0] for i in sim_scores]
            accounts_proxy_indices = [indices_proxy[i] for i in accounts_indices]

            _iloc = []
            _iloc.append(account_models.Profile.people.get(slug=targeted_account))
            for idx in accounts_proxy_indices:
                obj = account_models.Profile.people.get(slug=idx)
                _iloc.append(obj)
            return _iloc

def top_tags(*args, **kwargs):
    tags = post_models.PostTag.objects.all().annotate(
        num_count=Count('postitem__tags')
    ).order_by('-num_count')
    return tags