#!/usr/bin/env python2
# coding: utf8

import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse

from .forms import RegisterForm
from .models import PissUser
from .models import PissUserExtra
from .models import PissActiveCode

__author__ = 'lightless'
__email__ = 'root@lightless.me'


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(View):

    def get(self, request):
        background_number = random.choice(range(1, 9))
        context = {
            "background_number": background_number,
        }
        return render(request, "user_app/register.html", context)

    def post(self, request):

        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 表单验证成功
            # 1. 验证active code的可用性
            active_code_qs = PissActiveCode.objects.filter()
            # 2. 检查用户名和邮箱是否已经被注册
            # 3. 更新active code状态， 插入用户数据，extra数据
            # 4. 发送激活邮件
            # 5. 返回成功信息
            return JsonResponse(dict(code=1001, message=u"注册成功，请到邮箱检查激活邮件"))
        else:
            errors = register_form.errors
            for e in errors:
                return JsonResponse(dict(code=1004, message=errors[e][0]))
