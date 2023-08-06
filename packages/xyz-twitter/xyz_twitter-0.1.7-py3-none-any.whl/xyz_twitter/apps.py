#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:denishuang

from __future__ import unicode_literals

from django.apps import AppConfig


class Config(AppConfig):
    name = 'xyz_twitter'
    label = 'twitter'
    verbose_name = '推特'

    def ready(self):
        super(Config, self).ready()
        # from . import receivers