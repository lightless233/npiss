#!/usr/bin/env python2
# coding: utf8

import random

from django.shortcuts import render
from django.views import View

__author__ = 'lightless'
__email__ = 'root@lightless.me'


class IndexView(View):

    def get(self, request):
        background_image_number = random.choice(range(1, 9))
        context = {
            'background_number': background_image_number,
        }

        return render(request, "index_app/index.html", context)


