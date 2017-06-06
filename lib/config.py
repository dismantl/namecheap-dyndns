import ConfigParser
import os.path
from lib.domain import Domain
from lib.email import Email
from lib.logger import init_logger


class ConfigException(Exception):
    pass


class ConfigNotFound(ConfigException):
    pass


class ConfigMissingDomain(ConfigException):
    pass


class ConfigMissingParameter(ConfigException):
    pass


class ConfigEmptyParameter(ConfigException):
    pass


class Config:
    def __init__(self, file_name, search_dirs=['/']):
        '''read first found config file on search path and return domain objects'''
        # Defaults for general section:
        self.syslog = False
        self.logfile = None
        self.email = None

        self.domains = []
        self.config = ConfigParser.SafeConfigParser()

        search_dirs = map(os.path.expanduser, search_dirs)
        search_paths = []
        for search_dir in search_dirs:
            search_paths.append(os.path.join(search_dir,file_name))
        self.config_path = self.config.read(search_paths)
        if not self.config_path:
            raise ConfigNotFound(
                'no config found in search path {}'
                .format(', '.join(search_path))
            )

        for section in self.config.sections():
            if section == "general":
                self.parse_general_section(section)
            else:
                self.parse_domain_section(section)

        if not self.domains:
            raise ConfigMissingDomain(
                'no domains configured in {}'
                .format(self.config_path)
            )

    def parse_domain_section(self, section):
        required_parameters = ['hosts', 'password', 'ip']
        for parameter in required_parameters:
            # parameter missing
            if not self.config.has_option(section, parameter):
                raise ConfigMissingParameter(
                        'no {} parameter configured for {}'
                        .format(parameter,section)
                )
            # parameter empty
            elif not self.config.get(section, parameter):
                raise ConfigEmptyParameter(
                        'parameter {} is empty for domain {}'
                        .format(parameter,domain)
                )
        self.domains.append(Domain(
            section,
            self.config.get(section, 'hosts'),
            self.config.get(section, 'password'),
            self.config.get(section, 'ip')
        ))

    def parse_general_section(self, section):
        if self.config.has_option(section, "syslog") and self.config.getboolean(section, "syslog"):
            self.syslog = True
        if self.config.has_option(section, "logfile"):
            self.logfile = self.config.get(section, "logfile")
        if self.config.has_option(section, "email_server"):
            try:
                self.email = Email(
                    server = self.config.get(section, "email_server"),
                    fromaddr = self.config.get(section, "email_from"),
                    to = self.config.get(section, "email_to"),
                    user = self.config.get(section, "email_user"),
                    pw = self.config.get(section, "email_pw")
                )
            except ConfigParser.NoOptionError as e:
                raise ConfigMissingParameter(
                    "missing email parameter email_user or email_pw"
                )
        init_logger(self.syslog, self.logfile, self.email)
