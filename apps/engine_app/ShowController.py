#!/usr/bin/env python2
# coding: utf8

from __future__ import unicode_literals
from __future__ import print_function

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

__author__ = 'lightless'
__email__ = 'root@lightless.me'


@method_decorator(csrf_exempt, name="dispatch")
class ShowNormalImages(View):
    """
    显示原图接口，域名为piss的域名
    http://piss.lightless.me/i/image.png
    """

    @staticmethod
    def get(request, image_name):
        print(image_name)


@method_decorator(csrf_exempt, name="dispatch")
class ShowRedirectImages(View):
    """
    显示原图接口，域名为piss的域名，但是跳转到qiniu的链接
    http://piss.lightless.me/r/image.png
    """

    @staticmethod
    def get(request):
        pass


@method_decorator(csrf_exempt, name="dispatch")
class ShowThumbImages(View):
    """
    显示缩略图接口，域名为piss域名
    http://piss.lightless.me/t/image.png
    """

    @staticmethod
    def get(request):
        pass


@method_decorator(csrf_exempt, name="dispatch")
class ShowOriginImages(View):
    """
    直接显示原图接口，域名为qiniu域名
    http://qiniu.com/image.png
    """

    @staticmethod
    def get(request):
        """

        :param request:
        :return:
        """
        pass
