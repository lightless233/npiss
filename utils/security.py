#!/usr/bin/env python2
# coding: utf-8
# file: security.py.py
# time: 16-11-26 下午10:41

import socket
from struct import unpack
from urlparse import urlparse
from urlparse import urljoin

import requests

from logHelper import logger

__author__ = "lightless"
__email__ = "root@lightless.me"


def check_ssrf(url):
    """
    SSRF防御
    192.168.0.0/16
    10.0.0.0/8
    172.16.0.0/12
    127.0.0.0/8
    :param url: 待检测的URL
    :return: True：检查通过，不是SSRF， False：检查未通过，是SSRF
    """
    # 获取hostname和ip
    logger.debug("Start SSRF check, url: {0}".format(url))
    hostname = urlparse(url).hostname
    ip_address = socket.getaddrinfo(hostname, 'http')[0][4][0]
    logger.debug("Hostname: {0}, ip: {1}".format(hostname, ip_address))

    # 检查是否是内网IP
    try:
        long_ip = unpack("!L", socket.inet_aton(ip_address))[0]
    except socket.error:
        raise requests.exceptions.HTTPError
    # 按顺序分别检查: 127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    if long_ip >> 24 in [127, 10] or long_ip >> 20 in [44048] or long_ip >> 16 in [49320]:
        logger.warning("Found SSRF attack: {0}".format(url))
        return False

    return True


def safe_request(unsafe_url, **kwargs):
    """
    安全的获取URL内容，免受SSRF的攻击
    :param unsafe_url:
    :param kwargs:
    :return: None，有SSRF或者获取失败
    """

    def _request_check_location(r, *args, **kwargs):
        if not r.is_redirect:
            logger.debug("No SSRF Found: {0}".format(unsafe_url))
            return

        url = r.headers["location"]

        parsed = urlparse(url)
        url = parsed.geturl()
        if not parsed.netloc:
            url = urljoin(r.url, requests.utils.requote_uri(url))
        else:
            url = requests.utils.requote_uri(url)

        safe = check_ssrf(url)
        if not safe:
            raise requests.exceptions.InvalidURL("Found SSRF Attack: {0}".format(unsafe_url))

    t = check_ssrf(unsafe_url)
    if not t:
        raise requests.exceptions.InvalidURL("Found SSRF Attack: {0}".format(unsafe_url))

    all_hooks = kwargs.get('hooks', dict())
    if 'response' in all_hooks:
        if hasattr(all_hooks['response'], '__call__'):
            r_hooks = [all_hooks['response']]
        else:
            r_hooks = all_hooks['response']
        r_hooks.append(_request_check_location)
    else:
        r_hooks = [_request_check_location]

    all_hooks['response'] = r_hooks
    kwargs['hooks'] = all_hooks
    return requests.get(unsafe_url, **kwargs)


if __name__ == '__main__':

    def main():
        url = "http://lightless.me/info.php"
        r = safe_request(url)
        print r.content
    main()
