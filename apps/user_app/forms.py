#!/usr/bin/env python2
# coding: utf-8
# file: forms.py.py
# time: 16-11-29 下午10:40

from django import forms

__author__ = "lightless"
__email__ = "root@lightless.me"


class RegisterForm(forms.Form):

    username = forms.CharField(label="Username", min_length=2, max_length=64, error_messages={
        "required": u"用户名不能为空",
        'max_length': u"用户名不能超过64个字符",
        'min_length': u"用户名不能少于2个字符",
    })
    email = forms.EmailField(label="Email", error_messages={
        'required': u"邮箱不能为空",
        'invalid': u"请输入合法的邮箱地址",
    })
    password = forms.CharField(label="Password", min_length=6, max_length=64, error_messages={
        'required': u"密码不能为空",
        'max_length': u"密码不能超过64个字符",
        'min_length': u"密码不能少于6个字符",
    })
    active_code = forms.CharField(label="ActiveCode", max_length=64, min_length=64, error_messages={
        'required': u"激活码不能为空",
        'max_length': u"请输入正确的邀请码",
        'min_length': u"请输入正确的邀请码",
    })
