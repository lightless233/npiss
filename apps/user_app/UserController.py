#!/usr/bin/env python2
# coding: utf8

from __future__ import unicode_literals

import random
import threading
import base64
import hashlib
import datetime

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.utils import timezone

from .forms import RegisterForm
from .models import PissUser
from .models import PissUserExtra
from .models import PissActiveCode
from utils.CommonFunc import send_mail as send_mail_thread_func
from utils.logHelper import logger
from utils import CommonFunc

__author__ = 'lightless'
__email__ = 'root@lightless.me'


@method_decorator(csrf_exempt, name="dispatch")
class LoginView(View):

    @staticmethod
    def get(request):
        background_number = random.choice(range(1, 9))
        context = {
            "background_number": background_number,
        }
        return render(request, "user_app/login.html", context=context)

    @staticmethod
    def post(request):

        # todo 重构

        # 获取参数
        username_or_email = request.POST.get("username_or_email", "")
        if username_or_email == "":
            return JsonResponse(dict(code=1004, messsage=u"请输入用户名或密码"))
        password = request.POST.get("password", "")
        if password == "":
            return JsonResponse(dict(code=1004, message=u"请输入密码"))

        # 取出qs记录
        if "@" in username_or_email:
            qs = PissUser.objects.filter(email=username_or_email).first()
        else:
            qs = PissUser.objects.filter(username=username_or_email).first()

        if qs and qs.verify_password(password):

            if qs.status == 9001:
                return JsonResponse(dict(code=1004, message="用户未激活"))
            elif qs.status == 9003:
                return JsonResponse(dict(code=1004, message="用户被禁止登录"))
            elif qs.status == 9002:
                # 登录成功
                request.session["login"] = True
                request.session["user_id"] = qs.id
                request.session["username"] = qs.username

                # 更新最后登录时间和IP
                qs.last_login_ip = request.META.get("REMOTE_ADDR")
                qs.last_login_time = timezone.now()
                qs.save()

                return JsonResponse(dict(code=1001, message="登录成功，跳转中..."))
            else:
                return JsonResponse(dict(code=1004, message=u"用户名或密码错误"))

        else:
            return JsonResponse(dict(code=1004, message=u"用户名或密码错误"))


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
            ac = register_form.cleaned_data.get("active_code")
            active_code_qs = PissActiveCode.objects.filter(user_id=0, active_code=ac).first()
            if not active_code_qs:
                return JsonResponse(dict(code=1004, message=u"激活码无效"))

            # 2. 检查用户名和邮箱是否已经被注册
            username = register_form.cleaned_data.get("username")
            if "@" in username:
                return JsonResponse(dict(code=1004, message=u"用户名中不能含有@符号"))
            email = register_form.cleaned_data.get("email")
            user_qs = PissUser.objects.filter(Q(username=username) | Q(email=email)).exists()
            if user_qs:
                return JsonResponse(dict(code=1004, message=u"用户名或邮箱已存在"))

            # 3. 更新active code状态， 插入用户数据，extra数据
            # 3.1 插入用户数据
            new_user = PissUser()
            new_user.username = username
            new_user.email = email
            new_user.save_password(register_form.cleaned_data.get("password"))
            new_user.status = 9001
            new_user.token = CommonFunc.generate_random_string(64)
            new_user.save()
            # 3.2 插入用户extra数据
            new_user_extra = PissUserExtra()
            new_user_extra.user_id = new_user.id
            new_user_extra.save()
            # 3.3 更新激活码状态
            active_code_qs.user_id = new_user.id
            active_code_qs.used = True
            active_code_qs.used_time = datetime.datetime.now()
            active_code_qs.save()

            # 4. 发送激活邮件
            info = base64.b32encode(str(new_user.id) + "|" + new_user.email)
            sign = hashlib.md5(new_user.token + username + email).hexdigest()
            active_link = request.build_absolute_uri(reverse("validate_email")) + "?info={info}&sign={sign}"
            active_link = active_link.format(info=info, sign=sign)
            logger.info(active_link)

            send_mail_thread = threading.Thread(target=send_mail_thread_func, kwargs={"active_link": active_link})
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
        logger.debug("GET sign: {0}".format(sign))
        logger.debug("GET info: {0}".format(info))

        if sign == "":
            return JsonResponse(dict(code=1004, message=u"激活失败"))
        if info == "":
            return JsonResponse(dict(code=1004, message=u"激活失败"))

        context = {
            "code": 1004,
            "message": u"未知错误",
        }
        try:
            info = base64.b32decode(info).split("|")
            qs = PissUser.objects.filter(id=int(info[0].strip()), email=info[1].strip()).exclude(status=9002).first()
            if qs and sign == hashlib.md5(qs.token + qs.username + qs.email).hexdigest():
                qs.status = 9002
                qs.save()
                context = dict(
                    code=1001,
                    message=u"激活成功,将自动跳转到登录页...如果没有跳转，请点击<a href={url}>这里</a>".format(url=reverse("login"))
                )
            else:
                context = dict(code=1004, message=u"激活失败")
        except Exception as e:
            logger.error(e)
            context = dict(code=1004, message=u"激活失败")
        finally:
            return render(request, "user_app/validate_email.html", context=context)

