import unittest

from config_factory import ConfigFactory
from lib.config import ConfigNotFound, ConfigMissingDomain, ConfigMissingParameter, read_config


class TestNamecheapConfig(unittest.TestCase):

    def setUp(self):
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
            'domain': 'example.com',
            'password': 'test',
            'ip': '127.0.0.1'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no hosts parameter',
                read_config,
                config_path
        )

    def test_no_password(self):
        config_path = self.factory.create_config({
            'domain': 'example.com',
            'hosts': '@',
            'ip': '127.0.0.1'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no password parameter',
                read_config,
                config_path
        )

    def test_no_ip(self):
        config_path = self.factory.create_config({
            'domain': 'example.com',
            'hosts': '@',
            'password': 'test'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no ip parameter',
                read_config,
                config_path
        )

    def test_config_ok(self):
        config_path = self.factory.create_config({
            'domain': 'example.com',
            'hosts': '@, www',
            'password': 'test',
            'ip': '127.0.0.1'
        })
        domains = read_config(config_path)
        for domain in domains:
            assert domain.name == 'example.com'
            assert domain.hosts == ['@', 'www']
            assert domain.password == 'test'
            assert domain.ip == '127.0.0.1'

    def tearDown(self):
        self.factory.destroy_configs()
