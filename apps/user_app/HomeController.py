#!/usr/bin/env python2
# coding: utf-8
# file: HomeController.py
# time: 2016/12/31 16:16

from __future__ import unicode_literals
import random

from django.views import View
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect

from .models import PissUser
from utils import CommonFunc

__author__ = "lightless"
__email__ = "root@lightless.me"


class DashboardView(View):
    """
    用户中心 - 首页
    """

    @staticmethod
    def get(request):

        if request.session.get("login") is not True:
            return redirect("login")

        user_id = request.session.get("user_id")
        qs = PissUser.objects.filter(id=user_id).first()
        # 获取用户总上传图片数量
        total_image_num = 100

        # 获取用户上次登录时间
        last_login_time = qs.last_login_time.strftime("%Y-%m-%d %H:%M:%S")

        context = {
            'last_login_time': last_login_time,
        }
        return render(request, "user_app/home_index.html", context=context)


class ImageListView(View):
    """
    图片列表
    """

    @staticmethod
    def get(request):

        if request.session.get("login") is not True:
            return redirect("login")

        return render(request, "user_app/home_image_list.html")

    @staticmethod
    def post(request):
        pass


class LogoutView(View):
    """
    注销
    """

    @staticmethod
    def get(request):

        if request.session.get("login") is not True:
            return redirect("login")

        request.session.pop("user_id")
        request.session.pop("username")
        request.session.pop("login")
        return redirect('index')

