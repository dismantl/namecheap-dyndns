from lib.config import read_config
from lib.update import update_records


if __name__ == '__main__':
    config_file = 'namecheap.cfg'
    search_path = ['./', '~/', '/etc']

    domains = read_config(config_file, search_path, kill=True)

    for domain in domains:
        update_records(domain)
