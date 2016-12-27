#!/usr/bin/env python2
# coding: utf8

import random
import threading
import base64
import hashlib

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db.models import Q

from .forms import RegisterForm
from .models import PissUser
from .models import PissUserExtra
from .models import PissActiveCode
from utils.CommonFunc import send_mail as send_mail_thread_func
from utils.logHelper import logger

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

    @staticmethod
    def get(request):
        background_number = random.choice(range(1, 9))
        context = {
            "background_number": background_number,
        }
        return render(request, "user_app/register.html", context)

    @staticmethod
    def post(request):

        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 表单验证成功
            # 1. 验证active code的可用性
            print register_form.cleaned_data
            ac = register_form.cleaned_data.get("active_code")
            active_code_qs = PissActiveCode.objects.filter(user_id=0, active_code=ac)
            if not active_code_qs:
                return JsonResponse(dict(code=1004, message=u"激活码无效"))

            # 2. 检查用户名和邮箱是否已经被注册
            username = register_form.cleaned_data.get("username")
            email = register_form.cleaned_data.get("email")
            user_qs = PissUser.objects.filter(Q(username=username) | Q(email=email)).exists()
            if user_qs:
                return JsonResponse(dict(code=1004, message=u"用户名或邮箱已存在"))

            # 3. 更新active code状态， 插入用户数据，extra数据
            new_user = PissUser()
            new_user.username = username
            new_user.email = email
            new_user.save_password(register_form.cleaned_data.get("password"))
            new_user.status = 9001
            new_user.save()
            new_user_extra = PissUserExtra()
            new_user_extra.user_id = new_user.id
            new_user_extra.save()

            # 4. 发送激活邮件
            send_mail_thread = threading.Thread(target=send_mail_thread_func)
            send_mail_thread.start()

            # 5. 返回成功信息
            return JsonResponse(dict(code=1001, message=u"注册成功，请到邮箱检查激活邮件"))
        else:
            errors = register_form.errors
            for e in errors:
                return JsonResponse(dict(code=1004, message=errors[e][0]))


@method_decorator(csrf_exempt, name="dispatch")
class ValidEmailView(View):

    @staticmethod
    def get(request):
        # md5(token + username + email) = sign
        # info = base32(id + | + email)
        sign = request.GET.get("sign", "")
        info = request.GET.get("info", "")

        if sign == "":
            return JsonResponse(dict(code=1004, message=u"激活失败"))
        if info == "":
            return JsonResponse(dict(code=1004, message=u"激活失败"))

        try:
            info = base64.b32decode(info).split("|")
            qs = PissUser.objects.filter(id=int(info[0].strip()), email=info[1].strip()).exists()
            if qs:
                if sign == hashlib.md5(qs.token + qs.username + qs.email).hexdigest():
                    return JsonResponse(dict(code=1001, message=u"激活成功"))
            return JsonResponse(dict(code=1004, message=u"激活失败"))
        except Exception as e:
            logger.error(e)
            return JsonResponse(dict(code=1004, message=u"激活失败"))

