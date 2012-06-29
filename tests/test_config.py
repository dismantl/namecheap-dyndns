import unittest

from config_factory import ConfigFactory
from lib.config import ConfigNotFound, ConfigMissingDomain, ConfigMissingParameter, read_config


class TestNamecheapConfig(unittest.TestCase):

    def setUp(self):
        self.domain = 'example.com'
        self.password = 'test'
        self.hosts = '@, www'
        self.striped_hosts = map(lambda s: s.strip(), self.hosts.split(','))
        self.ip = '127.0.0.1'
        self.factory = ConfigFactory()

    def test_not_found(self):
        self.assertRaisesRegexp(
                ConfigNotFound,
                'no config found',
                read_config,
                'not_exists.cfg'
        )

    def test_no_sections(self):
        config_path = self.factory.create_config()
        self.assertRaisesRegexp(
                ConfigMissingDomain,
                'no domains configured',
                read_config,
                config_path
        )

    def test_no_hosts(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'password': self.password,
            'ip': self.ip
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no hosts parameter',
                read_config,
                config_path
        )

    def test_no_password(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': '@',
            'ip': self.ip
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no password parameter',
                read_config,
                config_path
        )

    def test_no_ip(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': '@',
            'password': self.password
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no ip parameter',
                read_config,
                config_path
        )

    def test_config_ok(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': self.hosts,
            'password': self.password,
            'ip': self.ip
        })
        domains = read_config(config_path)
        for domain in domains:
            self.assertEqual(domain.name, self.domain)
            self.assertListEqual(domain.hosts, self.striped_hosts)
            self.assertEqual(domain.password, self.password)
            self.assertEqual(domain.ip, self.ip)

    def tearDown(self):
        self.factory.destroy_configs()
