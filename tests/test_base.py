# -*- coding: utf-8 -*-
import requests_mock
import requests
import json
from unittest import TestCase
from ofrestapi import exception, base


class BaseClassTestCase(TestCase):
    test_url = 'http://localhost/test/url'
    host = 'http://localhost/'

    @requests_mock.Mocker()
    def test__submit_request_headers(self, m):
        m.register_uri('GET',
                       self.test_url,
                       status_code=200)

        req = base.Base(self.host, 'secret', '/test/url')
        req._submit_request(requests.get, 'test/url')

        self.assertTrue(m.called)
        self.assertIn('Authorization', m.last_request.headers)
        self.assertEqual(m.last_request.headers['Authorization'], 'secret')

    @requests_mock.Mocker()
    def test__submit_request_exception_map(self, m):
        m.register_uri('GET',
                       self.test_url,
                       status_code=419,
                       text=json.dumps({
                           'exception': 'UserAlreadyExistsException',
                           'message': 'An error message'
                       }))

        with self.assertRaises(exception.UserAlreadyExistsException):
            req = base.Base(self.host, 'secret', '/test/url')
            req._submit_request(requests.get, 'test/url')
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test__submit_request_unmapped_exception(self, m):
        m.register_uri('GET',
                       self.test_url,
                       status_code=419,
                       text=json.dumps({
                           'exception': 'SomeUnmappedException',
                           'message': 'An error message'
                       }))

        with self.assertRaises(exception.InvalidResponseException):
            req = base.Base(self.host, 'secret', '/test/url')
            req._submit_request(requests.get, 'test/url')
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test__submit_request_undeclared_exception(self, m):
        m.register_uri('GET',
                       self.test_url,
                       status_code=419,
                       text=json.dumps({}))

        with self.assertRaises(exception.InvalidResponseException):
            req = base.Base('http://localhost/', 'secret', '/test/url')
            req._submit_request(requests.get, 'test/url')

    @requests_mock.Mocker()
    def test__submit_request_json_success(self, m):
        payload = {
            'key1': 'value1',
            'key2': 'value2'
        }
        m.register_uri('GET',
                       self.test_url,
                       text=json.dumps(payload))

        req = base.Base(self.host, 'secret', '/test/url')
        result = req._submit_request(requests.get, 'test/url')

        self.assertIs(type(result), dict)
        self.assertDictEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test__submit_request_empty_success(self, m):
        m.register_uri('GET',
                       self.test_url)

        req = base.Base(self.host, 'secret', '/test/url')
        result = req._submit_request(requests.get, 'test/url')

        self.assertIs(type(result), bool)
        self.assertTrue(result)
        self.assertTrue(m.called)


