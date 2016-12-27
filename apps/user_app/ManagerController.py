#!/usr/bin/env python2
# coding: utf-8
# file: ManagerController.py
# time: 2016/12/27 22:37

import random

from django.views import View
from django.conf import settings
from django.http import JsonResponse

from .models import PissActiveCode
from utils import CommonFunc

__author__ = "lightless"
__email__ = "root@lightless.me"


class GenerateACView(View):
    """
    生成邀请码所用的API
    """

    @staticmethod
    def get(request):
        token = request.GET.get("token", "")
        if token != settings.MANAGE_TOKEN:
            return JsonResponse(dict(dict=1004, message=u"Fuck You Hacker!"))
        num = request.GET.get("num", 1)
        length = request.GET.get("length", 16)

        ac_list = list()
        for x in xrange(int(num)):
            new_ac = PissActiveCode()
            new_ac.active_code = CommonFunc.generate_random_string(length=int(length))
            new_ac.save()
            ac_list.append(new_ac.active_code)
        return JsonResponse(dict(code=1001, message=u"成功生成邀请码", ac_list=ac_list))


class QueryACView(View):
    """
    获取邀请码所用的API
    """

    @staticmethod
    def get(request):
        token = request.GET.get("token", "")
        if token != settings.MANAGE_TOKEN:
            return JsonResponse(dict(dict=1004, message=u"Fuck You Hacker!"))
        num = request.GET.get("num", 1)
        num = int(num)

        qs = PissActiveCode.objects.filter(used=0, user_id=0).all()
        pool = list()
        ac_list = list()

        for q in qs:
            pool.append(q.active_code)

        for x in xrange(num):
            index = random.randint(0, len(pool)-1)
            ac_list.append(pool[index])
            pool.remove(pool[index])

        return JsonResponse(dict(code=1001, message=u"获取成功", ac_list=ac_list))


