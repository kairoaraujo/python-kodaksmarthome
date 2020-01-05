#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2019, 2020 Kairo de Araujo
#
from requests.status_codes import codes

# DEVICES EVENTS
DEVICE_EVENT_MOTION = 1
DEVICE_EVENT_SOUND = 2
DEVICE_EVENT_BATTERY = 7

# REGION_URLS
SUPPORTED_REGIONS = {
    "EU": {
        "URL": "https://app-eu.kodaksmarthome.com/web",
        "URL_TOKEN": "https://api-t01-r3.perimetersafe.com/v1/oauth/token",
        "URL_AUTH": "https://app-eu.kodaksmarthome.com/web/authenticate",
        "URL_DEVICES": "https://app-eu.kodaksmarthome.com/web/user/device",
        "URL_LOGOUT": "https://app-eu.kodaksmarthome.com/web/#/user/logout",
    }
}


class _URLS(object):
    def __init__(self, region):
        self.__dict__ = region


# HTTP General
HTTP_CODE = codes

# HTTP_CLIENT
HTTP_CLIENT_MODEL = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36"
)
HTTP_CLIENT_AUTHORIZATION = (
    "Basic MjFmOTk1M2VlZGE4N2I3MGRjMTE1ZTUyNDU2ODE1OWNjNmExNzI2MTNiOGUyMGMwMT"
    + "UzMGZjNjg2ODc3Mzk2ZDo0ZDA5YmZlMWRhMjU0YmRjNzA4YjEzMGIxMzVmYzA2NjU4ODI2"
    + "MWZjNTY2YWQzMWEyMGM1YjA5ZTY3NTFkNTgy"
)


# HTTP_HEADERS
HTTP_HEADERS_BASIC = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Origin": "https://app-eu.kodaksmarthome.com",
    "Referer": "https://app-eu.kodaksmarthome.com/web/",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": HTTP_CLIENT_MODEL,
}
HTTP_HEADERS_AUTH = {
    **HTTP_HEADERS_BASIC,
    **{"Content-Type": "application/x-www-form-urlencoded"},
    **{"Authorization": HTTP_CLIENT_AUTHORIZATION},
}
HTTP_HEADERS_OPTIONS = {
    "Access-Control-Request-Method": "POST",
    "Access-Control-Request-Headers": "authorization",
    "Authorization": None,
}
