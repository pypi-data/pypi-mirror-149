# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from django.conf import settings
from time import sleep

CONF = getattr(settings, 'TWITTER', {})
import tweepy


class Api(object):

    def __init__(self, conf=CONF):
        self.conf = conf
        self.auth = auth = tweepy.OAuth1UserHandler(
            conf["CONSUMER_KEY"],
            conf["CONSUMER_KEY_SECRET"],
            conf["ACCESS_TOKEN"],
            conf["ACCESS_TOKEN_SECRET"]
        )
        self.api = tweepy.API(auth)

    def get_user(self, username):
        return self.api.get_user(screen_name=username)

    def get_tweets(self, uid):
        return tweepy.Cursor(
            self.api.user_timeline,
            id=uid,
            tweet_mode="extended",
            wait_on_rate_limit=True,
            count=200  # limit to 200 tweets per page
        ).items()

    def serialize_user(self, u):
        fs = ['id', 'name', 'screen_name', 'url', 'profile_image_url_https', 'description', 'created_at',
              'friends_count', 'favourites_count', 'followers_count', ]
        return dict([(f, getattr(u, f)) for f in fs])

    def serialize_tweet(self, t):
        fs = ['id', 'full_text', 'created_at', 'favorite_count']
        d = dict([(f, getattr(t, f)) for f in fs])
        d['user_id'] = t.user.id
        return d


def update_or_create_user(screen_name):
    api = Api()
    u = api.get_user(screen_name)
    from .models import User
    user, created = User.objects.update_or_create(screen_name=screen_name, defaults=dict(
        tid=u.id_str, name=u.name, url=u.url, avatar=u.profile_image_url_https, description=u.description,
        created_at=u.created_at.replace(tzinfo=None), detail=api.serialize_user(u)
    ))
    return user


def sync_user_tweets(user):
    from .helper import Api
    api = Api()
    u = api.get_user(user.screen_name)
    for t in api.get_tweets(u.id_str):
        user.tweets.update_or_create(
            tid=t.id_str, defaults=dict(
                tid=t.id_str,
                full_text=t.full_text,
                created_at=t.created_at.replace(tzinfo=None),
                favorite_count=t.favorite_count,
                retweet_count=t.retweet_count
            )
        )


class TwitterScan(object):

    def __init__(self, callback=print):
        from xyz_util.crawlutils import Browser
        self.browser = Browser()
        self.browser.get('https://www.twitter.com/explore')

    def login(self, account=CONF.get('BROWSER_EMAIL', ''), password=None):
        self.browser.element('a[data-testid="loginButton"]').click()
        sleep(2)
        e = self.browser.element('input[autocomplete="username"]')
        self.browser.clean_with_send(e, account)
        if account:
            self.browser.driver.find_elements_by_css_selector('div[role="button"]')[2].click()
            if password:
                e = self.browser.element('input[name="password"]')
                self.browser.clean_with_send(e, password)
                self.browser.element('div[role="button"]').click()

    def search_screen_name(self, name):
        e = self.browser.element('input[enterkeyhint="search"]')
        self.browser.clean_with_send(e, name)
        e2 = self.browser.element('div[aria-multiselectable]')
        sleep(2)
        rs = self.browser.element_to_bs(e2).select('div[data-testid="typeaheadResult"]')
        for r in rs[1:]:
            for a in r.select('span'):
                if a.text.startswith('@'):
                    return a.text[1:]
