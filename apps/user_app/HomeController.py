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

from .models import PissActiveCode
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

        return render(request, "user_app/home_index.html")


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

