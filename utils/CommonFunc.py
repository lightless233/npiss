#!/usr/bin/env python2
# coding: utf-8
# file: CommonFunc.py.py
# time: 16-11-26 下午11:25

import string
import random

__author__ = "lightless"
__email__ = "root@lightless.me"


def format_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        return "http://" + url
    else:
        return url


def generate_random_string(length=12):
    pool = string.ascii_letters + string.digits
    return "".join([random.choice(pool) for i in range(length)])


def send_mail(active_link=None):
    pass


if __name__ == '__main__':
    def main():
        print generate_random_string()
    main()
