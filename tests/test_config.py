import unittest
import lib.config

from config_factory import ConfigFactory


class TestNamecheapConfig(unittest.TestCase):

    def setUp(self):
        self.domain = 'example.com'
        self.password = 'test'
        self.hosts = '@, www'
        self.striped_hosts = map(lambda s: s.strip(), self.hosts.split(','))
        self.ip = '127.0.0.1'
        self.factory = ConfigFactory()

    def test_not_found(self):
        with self.assertRaises(lib.config.ConfigNotFound):
            lib.config.read_config('does_not_exist.cfg')

    def test_no_sections(self):
        config_path = self.factory.create_config()
        with self.assertRaises(lib.config.ConfigMissingDomain):
            lib.config.read_config(config_path)

    def test_no_hosts(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'password': self.password,
            'ip': self.ip
        })
        with self.assertRaises(lib.config.ConfigMissingParameter):
            lib.config.read_config(config_path)

    def test_empty_hosts(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': '',
            'password': self.password,
            'ip': self.ip
        })
        with self.assertRaises(lib.config.ConfigEmptyParameter):
            lib.config.read_config(config_path)

    def test_no_password(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': '@',
            'ip': self.ip
        })
        with self.assertRaises(lib.config.ConfigMissingParameter):
            lib.config.read_config(config_path)

    def test_empty_password(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': self.hosts,
            'password': '',
            'ip': self.ip
        })
        with self.assertRaises(lib.config.ConfigEmptyParameter):
            lib.config.read_config(config_path)

    def test_no_ip(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': '@',
            'password': self.password
        })
        with self.assertRaises(lib.config.ConfigMissingParameter):
            lib.config.read_config(config_path)

    def test_empty_ip(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': self.hosts,
            'password': self.password,
            'ip': ''
        })
        with self.assertRaises(lib.config.ConfigEmptyParameter):
            lib.config.read_config(config_path)

    def test_config_ok(self):
        config_path = self.factory.create_config({
            'domain': self.domain,
            'hosts': self.hosts,
            'password': self.password,
            'ip': self.ip
        })
        domains = lib.config.read_config(config_path)
        for domain in domains:
            self.assertEqual(domain.name, self.domain)
            self.assertListEqual(domain.hosts, self.striped_hosts)
            self.assertEqual(domain.password, self.password)
            self.assertEqual(domain.ip, self.ip)

    def tearDown(self):
        self.factory.destroy_configs()
