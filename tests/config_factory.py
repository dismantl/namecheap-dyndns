import ConfigParser
import os


CONFIG_FILE = 'namecheap.cfg'


def create_config(*domains):
    section_name = 'domain'
    config = ConfigParser.SafeConfigParser()

    for domain in domains:
        if section_name in domain:
            config.add_section(domain[section_name])

            for key in filter(lambda key: key != section_name, domain.keys()):
                config.set(domain[section_name], key, domain[key])

    with open(CONFIG_FILE, 'w') as testconfig:
        config.write(testconfig)


def destroy_config():
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)
