import unittest

import requests
from mock import patch

import lib.check


class TestCheckIp(unittest.TestCase):

    def setUp(self):
        self.localhost = '127.0.0.1'

    def test_success(self):
        with patch.object(requests, 'get'):
            requests.get.return_value.content = self.localhost
            self.assertEqual(lib.check.check_ip(), self.localhost)

    def test_parse_exception(self):
        with patch.object(requests, 'get'):
            requests.get.return_value.content = 'no ip here'
            with self.assertRaises(lib.check.CheckIpParseException):
                lib.check.check_ip()

    def test_cached(self):
        self.assertIsNone(lib.check.cached)
        with patch.object(requests, 'get'):
            requests.get.return_value.content = self.localhost
            lib.check.check_ip()
            self.assertIsNotNone(lib.check.cached)

    def tearDown(self):
        lib.check.cached = None
