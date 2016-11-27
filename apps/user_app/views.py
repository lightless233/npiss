#!/usr/bin/env python2
# coding: utf8

import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

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
        pass
