import re

import requests


cached = None
CHECK_IP_URL = 'http://checkip.dyndns.com'


class CheckIpException(Exception):
    pass


class CheckIpRequestException(CheckIpException):
    pass


class CheckIpParseException(CheckIpException):
    pass


def check_ip():
    global cached
    if cached:
        return cached

    try:
        r = requests.get(CHECK_IP_URL)
    except requests.RequestException as e:
        raise CheckIpRequestException(e.message)

    s = re.search('(\d{1,3}\.?){4}', r.content)
    if s:
        cached = s.group()
        return cached

    raise CheckIpParseException('no ip address found in response {}'.format(r.content))
