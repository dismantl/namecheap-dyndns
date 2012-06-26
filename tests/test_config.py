import unittest

from config_factory import create_config, destroy_config, CONFIG_FILE
from lib.config import ConfigNotFound, ConfigMissingDomain, ConfigMissingParameter, read_config


class TestNamecheapConfig(unittest.TestCase):

    def test_not_found(self):
        self.assertRaisesRegexp(
                ConfigNotFound,
                'no config found',
                read_config,
                'not_exists.cfg'
        )

    def test_no_sections(self):
        create_config()
        self.assertRaisesRegexp(
                ConfigMissingDomain,
                'no domains configured',
                read_config,
                CONFIG_FILE
        )

    def test_no_hosts(self):
        create_config({
            'domain': 'example.com',
            'password': 'test',
            'ip': '127.0.0.1'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no hosts parameter',
                read_config,
                CONFIG_FILE
        )

    def test_no_password(self):
        create_config({
            'domain': 'example.com',
            'hosts': '@',
            'ip': '127.0.0.1'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no password parameter',
                read_config,
                CONFIG_FILE
        )

    def test_no_ip(self):
        create_config({
            'domain': 'example.com',
            'hosts': '@',
            'password': 'test'
        })
        self.assertRaisesRegexp(
                ConfigMissingParameter,
                'no ip parameter',
                read_config,
                CONFIG_FILE
        )

    def test_config_ok(self):
        create_config({
            'domain': 'example.com',
            'hosts': '@, www',
            'password': 'test',
            'ip': '127.0.0.1'
        })
        domains = read_config(CONFIG_FILE)
        for domain in domains:
            assert domain.name == 'example.com'
            assert domain.hosts == ['@', 'www']
            assert domain.password == 'test'
            assert domain.ip == '127.0.0.1'

    def tearDown(self):
        destroy_config()
