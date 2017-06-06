import argparse
import requests
import re
from lib.config import Config
from lib.check import check_ip
from lib.logger import log_err, log_msg


UPDATE_NAMECHEAP_URL = 'https://dynamicdns.park-your-domain.com/update'


def update_records(domain):
    ip = domain.ip if domain.ip != 'check' else check_ip()
    for host in domain.hosts:
        resp = requests.get(UPDATE_NAMECHEAP_URL, params={
            'domain': domain.name,
            'host': host,
            'password': domain.password,
            'ip': ip
        }, timeout=1)
        if resp.status_code != 200 or not re.search('<ErrCount>0<\/ErrCount>',resp.text):
            log_err('Namecheap responded to request with status {} and message {}'
                .format(resp.status_code, resp.text))
        else:
            log_msg('Successfully updated IP for {}.{} to {}'.format(host,domain.name,ip))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Namecheap dynamic DNS updater')
    parser.add_argument('--config', '-c', default='namecheap.cfg',
        help="Configuration file path. Default: search in ./, ~/, /etc")
    args = parser.parse_args()

    search_path = ['./', '~/', '/etc']

    config = Config(args.config, search_path)

    for domain in config.domains:
        update_records(domain)
