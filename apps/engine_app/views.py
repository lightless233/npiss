#!/usr/bin/env python2
# coding: utf8

from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

__author__ = 'lightless'
__email__ = 'root@lightless.me'


@method_decorator(csrf_exempt, name="dispatch")
class ApiUploadImageView(View):

    def post(self, request):
        print request.POST
        return JsonResponse({"foo": "bar"})


@method_decorator(csrf_exempt, name="dispatch")
class ApiUploadURLView(View):

    def post(self, request):
        print request.POST
        url = request.POST.get("url", "")
        if url == "":
            return JsonResponse(dict(code=1004, message=u"URL不能为空"))

        # Check SSRF

        return HttpResponse("hello")

