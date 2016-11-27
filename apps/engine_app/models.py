#!/usr/bin/env python2
# coding: utf8

from __future__ import unicode_literals

from django.db import models

__author__ = 'lightless'
__email__ = 'root@lightless.me'


class PissImages(models.Model):

    class Meta:
        db_table = "piss_images"

    user_id = models.BigIntegerField()
    qiniu_url = models.CharField(max_length=512)
    piss_url = models.CharField(max_length=32, unique=True)
    local_filename = models.CharField(max_length=64, unique=True, default=None)
    created_time = models.DateTimeField(auto_created=True, default=None)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

