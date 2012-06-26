import requests

from lib.config import read_config


if __name__ == '__main__':
    config_file = 'namecheap.cfg'
    search_path = ['./', '~/', '/etc']

    domains = read_config(config_file, search_path, kill=True)

    for domain in domains:
        for host in domain.hosts:
            try:
                r = requests.get('https://dynamicdns.park-your-domain.com/update', params={
                    'domain': domain.name,
                    'host': host,
                    'password': domain.password,
                    'ip': domain.ip
                }, timeout=1)
            except requests.ConnectionError as e:
                print e.message
