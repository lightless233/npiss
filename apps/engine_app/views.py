#!/usr/bin/env python2
# coding: utf8

import os
from StringIO import StringIO
from PIL import Image

from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from requests.exceptions import InvalidURL
from requests.exceptions import HTTPError

from .models import PissImages
from utils.security import safe_request
from utils.logHelper import logger
from utils.CommonFunc import format_url
from utils.CommonFunc import generate_random_string

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

        # 使用safe_request免受SSRF攻击
        url = format_url(url)
        try:
            r = safe_request(url, stream=True)
        except InvalidURL:
            logger.warning("SSRF Attack: {0}".format(url))
            return JsonResponse(dict(code=1003, message=u"SSRF Attack Found!"))
        except HTTPError:
            logger.warning("Invalid URL: {0}".format(url))
            return JsonResponse(dict(code=1003, message=u"请输入正确的URL"))

        code = r.status_code
        content_type = r.headers.get("Content-Type", "")

        logger.info("GET {url} - {code} - {type}".format(url=url, code=r.status_code, type=r.headers["Content-Type"]))
        if code == 200 and "image" in content_type:
            # 下载图片到临时文件夹
            tmp_path = settings.IMAGE_TMP_PATH
            thumb_path = settings.IMAGE_THUMB_PATH
            if not os.path.exists(tmp_path):
                os.mkdir(tmp_path)
            if not os.path.exists(thumb_path):
                os.mkdir(thumb_path)
            tmp_filename = generate_random_string()
            i = Image.open(StringIO(r.content))
            # 存储图片原图
            i.save(os.path.join(tmp_path, tmp_filename + "." + i.format.lower()))
            logger.info("Save to {0}".format(os.path.join(tmp_path, tmp_filename + "." + i.format.lower())))
            # 存储缩略图
            i.thumbnail((128, 128))
            i.save(os.path.join(thumb_path, tmp_filename + "." + i.format.lower()))

            # 获取当前用户user_id
            # todo: save to database

        else:
            return JsonResponse(dict(code=1004, message=u"请输入正确的URL"))

        return HttpResponse("hello")

