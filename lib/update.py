import requests

from lib.check import check_ip


UPDATE_NAMECHEAP_URL = 'https://dynamicdns.park-your-domain.com/update'


def update_records(domain):
    ip = domain.ip if domain.ip != 'check' else check_ip()
    for host in domain.hosts:
        requests.get(UPDATE_NAMECHEAP_URL, params={
            'domain': domain.name,
            'host': host,
            'password': domain.password,
            'ip': ip
        }, timeout=1)
