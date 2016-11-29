#!/usr/bin/env python2
# coding: utf8

from __future__ import unicode_literals

from django.db import models

__author__ = 'lightless'
__email__ = 'root@lightless.me'


class PissUser(models.Model):
    """
    存储用户信息
    """

    class Meta:
        db_table = "piss_users"

    username = models.CharField(max_length=64, null=False, blank=False, unique=True)
    password = models.CharField(max_length=512, null=False, blank=False)
    email = models.CharField(max_length=64, null=False, blank=False, unique=True)
    token = models.CharField(max_length=64, unique=True, default="")
    status = models.PositiveSmallIntegerField(default=0, blank=False, null=False)
    created_time = models.DateTimeField(auto_created=True, default=None)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_user_status(self):
        status_dict = {
            9001: {"message": u"用户未激活",},
            9002: {"message": u"用户正常", },
            9003: {"message": u"用户被禁止登录", },
        }

        return status_dict[self.status]

    def __str__(self):
        return "<{username}, {status}>".format(username=self.username, status=self.get_user_status())


class PissActiveCode(models.Model):
    """
    存储激活码信息
    """

    class Meta:
        db_table = "piss_active_code"

    user_id = models.BigIntegerField(null=False, blank=False)
    active_code = models.CharField(max_length=64, null=False, blank=False, unique=True)
    used = models.BooleanField(null=False, blank=False, default=False)
    used_time = models.DateTimeField(default=None)
    created_time = models.DateTimeField(auto_created=True, default=None)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_code_status(self):
        code_status = {
            True: u"激活码已失效",
            False: u"激活码有效",
        }
        return code_status[self.used]

    def use_active_code(self):
        self.used = True

    def __str__(self):
        return "<{code}-{used}>".format(code=self.active_code, used=self.used)


class PissUserExtra(models.Model):
    """
    存储用户额外信息
    """
    class Meta:
        db_table = "piss_user_extra"

    user_id = models.BigIntegerField()
    access_key = models.CharField(max_length=40, blank=True)
    secret_key = models.CharField(max_length=40, blank=True)
    domain = models.CharField(max_length=255)

    # 如果该字段为true，则使用qiniu相关的信息和链接
    # 如果该字段为False，则使用本站url,302到七牛链接
    use_qiniu = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_created=True, default=None)
    updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "<{user}-{qiniu}>".format(user=self.use_id, qiniu=self.use_qiniu)


