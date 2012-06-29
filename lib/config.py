import ConfigParser
import os.path
from lib.domain import Domain


class ConfigException(RuntimeError):
    pass


class ConfigNotFound(ConfigException):
    pass


class ConfigMissingDomain(ConfigException):
    pass


class ConfigMissingParameter(ConfigException):
    pass


class ConfigEmptyParameter(ConfigException):
    pass


def config_error(kill, exception, msg, *args):
    '''print error and exit or raise exception'''
    msg = msg.format(*args)
    if kill:
        print msg
        exit(1)
    else:
        raise exception(msg)


def read_config(file_name, search_path=['./'], kill=False):
    '''read first found config file on search path and return domain objects'''
    required_parameters = ['hosts', 'password', 'ip']
    config = ConfigParser.SafeConfigParser()

    for path in map(os.path.expanduser, search_path):
        config_path = os.path.join(path, file_name)
        if os.path.exists(config_path):
            config.read(config_path)
            if config.sections():
                for domain in config.sections():
                    for parameter in required_parameters:
                        # parameter missing
                        if not config.has_option(domain, parameter):
                            config_error(
                                    kill,
                                    ConfigMissingParameter,
                                    'no {} parameter configured for {}',
                                    parameter,
                                    domain
                            )
                        # parameter empty
                        elif not config.get(domain, parameter):
                            config_error(
                                    kill,
                                    ConfigEmptyParameter,
                                    'parameter {} is empty for domain {}',
                                    parameter,
                                    domain
                            )
                # skip else block of for loop
                break
            else:
                config_error(
                        kill,
                        ConfigMissingDomain,
                        'no domains configured in {}',
                        config_path
                )
    else:
        config_error(
                kill,
                ConfigNotFound,
                'no config found in search path {}',
                ', '.join(search_path)
        )

    domains = []
    for domain in config.sections():
        domains.append(Domain(
            domain,
            config.get(domain, 'hosts'),
            config.get(domain, 'password'),
            config.get(domain, 'ip')
        ))
    return domains
