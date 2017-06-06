import re
import requests

CHECK_IP_URL = 'https://ip.mayfirst.org'


class CheckIpException(Exception):
    pass


class CheckIpRequestException(CheckIpException):
    pass


class CheckIpParseException(CheckIpException):
    pass


def check_ip():
    try:
        r = requests.get(CHECK_IP_URL)
    except requests.RequestException as e:
        raise CheckIpRequestException(e.message)

    if re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', r.content):
        return r.content

    raise CheckIpParseException('no ip address found in response {}'.format(r.content))
