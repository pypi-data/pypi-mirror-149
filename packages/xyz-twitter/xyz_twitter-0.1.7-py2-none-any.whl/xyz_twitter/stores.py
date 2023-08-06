# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from xyz_util.mongoutils import Store


class UserStore(Store):
    name = 'twitter_user'


class TweetStore(Store):
    name = 'twitter_tweet'
