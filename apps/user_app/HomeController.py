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
        return render(request, "user_app/home_index.html")


class ImageListView(View):
    """
    图片列表
    """

    @staticmethod
    def get(request):
        return render(request, "user_app/home_image_list.html")

    @staticmethod
    def post(request):
        pass


