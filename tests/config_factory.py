import ConfigParser
import os
import tempfile


class ConfigFactory(object):
    '''create and destroy test configs'''
    def __init__(self):
        self.config_paths = []

    def create_config(self, *domains):
        section_name = 'domain'
        config = ConfigParser.SafeConfigParser()
        _, config_path = tempfile.mkstemp(prefix='namecheap')

        for domain in domains:
            if section_name in domain:
                config.add_section(domain[section_name])

                for key in filter(lambda key: key != section_name, domain.keys()):
                    config.set(domain[section_name], key, domain[key])

        with open(config_path, 'w') as testconfig:
            config.write(testconfig)

        self.config_paths.append(config_path)

        return config_path

    def destroy_configs(self):
        while self.config_paths:
            config_path = self.config_paths[-1]
            if os.path.exists(config_path):
                os.remove(config_path)
            self.config_paths.pop()
