#!/usr/bin/env python2
# coding: utf8

import os
import platform
from cStringIO import StringIO
from PIL import Image

from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
from requests.exceptions import InvalidURL
from requests.exceptions import HTTPError
import qiniu
import qiniu.config

from .models import PissImages
from ..user_app.models import PissUser
from ..user_app.models import PissUserExtra
from utils.security import safe_request
from utils.logHelper import logger
from utils.CommonFunc import format_url
from utils.CommonFunc import generate_random_string

__author__ = 'lightless'
__email__ = 'root@lightless.me'


@method_decorator(csrf_exempt, name="dispatch")
class ApiUploadImageView(View):

    @staticmethod
    def post(request):

        # 获取当前用户信息
        is_login = request.session.get("login", None)
        user_id = request.session.get("user_id") if is_login is True else 1

        # 获取用户的七牛信息
        qs = PissUserExtra.objects.filter(user_id=user_id).first()
        if not qs:
            return JsonResponse(dict(code=1004, message="用户不存在"))
        access_key = qs.access_key
        secret_key = qs.secret_key
        bucket_name = qs.bucket_name
        if access_key == "" or secret_key == "" or bucket_name == "":
            return JsonResponse(dict(code=1004, message="未设置七牛SDK秘钥"))

        # 处理用户上传的文件
        images = request.FILES["file_data"]

        if "image" not in images.content_type:
            return JsonResponse(dict(code=1004, message=u"图片格式错误"))

        tmp_filename = generate_random_string()
        raw_images = StringIO()
        for chunk in images.chunks():
            raw_images.write(chunk)

        # 根据不同平台读取不同的配置
        if "Windows" in platform.system():
            tmp_path = settings.WIN_IMAGE_TMP_PATH
            thumb_path = settings.WIN_IMAGE_THUMB_PATH
        else:
            tmp_path = settings.IMAGE_TMP_PATH
            thumb_path = settings.IMAGE_THUMB_PATH
        if not os.path.exists(tmp_path):
            os.mkdir(tmp_path)
        if not os.path.exists(thumb_path):
            os.mkdir(thumb_path)
        try:
            i = Image.open(raw_images)
        except IOError:
            return JsonResponse(dict(code=1004, message=u"图片格式错误"))
        # 存储图片原图
        suffix = i.format.lower().replace("jpeg", "jpg")
        local_file = os.path.join(tmp_path, tmp_filename + "." + suffix)
        i.save(local_file)
        logger.info("Save to {0}".format(local_file))

        # 存储缩略图
        i.thumbnail((128, 128))
        i.save(os.path.join(thumb_path, tmp_filename + "." + suffix))

        # 上传到七牛
        qiniu_auth = qiniu.Auth(access_key, secret_key)
        qiniu_filename = generate_random_string(6) + "." + suffix
        token = qiniu_auth.upload_token(bucket_name, qiniu_filename, 3600)
        ret, info = qiniu.put_file(token, qiniu_filename, local_file)
        if ret['key'] != qiniu_filename:
            return JsonResponse(dict(code=1004, message="上传到七牛失败"))

        # 存储到数据库
        p_image = PissImages()
        p_image.user_id = user_id
        p_image.qiniu_filename = qiniu_filename
        p_image.local_filename = local_file
        qiniu_url = qs.domain + "/" + qiniu_filename
        p_image.qiniu_url = qiniu_url
        p_image.piss_url = settings.DOMAIN + qiniu_filename
        p_image.save()

        return JsonResponse(dict(code=1001, message=u"上传成功", url=qiniu_url))


@method_decorator(csrf_exempt, name="dispatch")
class ApiUploadURLView(View):

    @staticmethod
    def post(request):

        return JsonResponse(dict(code=1004, message="该功能尚未开放，敬请期待"))

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
        if int(code) == 200 and "image" in content_type:
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

            # todo: 获取当前用户user_id
            # todo: save to database
            return JsonResponse(dict(code=1001, message=u"上传成功"))

        else:
            return JsonResponse(dict(code=1004, message=u"请输入正确的URL"))

