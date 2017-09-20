# -*- coding: utf-8 -*-
import requests_mock
import json
from unittest import TestCase
from ofrestapi import system


class SystemTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/system/properties'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.system = system.System(self.host, '1234')

    @requests_mock.Mocker()
    def test_get_props(self, m):
        payload = {
            "properties": [{
                "value": "value1",
                "key": "key1"
            }]
        }

        m.register_uri('GET',
                       self.url,
                       text=json.dumps(payload)
                       )

        result = self.system.get_props()

        self.assertDictEqual(result, payload)

    @requests_mock.Mocker()
    def test_get_prop(self, m):
        payload = {
            "value": "value1",
            "key": "key1"
        }

        m.register_uri('GET',
                       self.url + '/key1',
                       text=json.dumps(payload)
                       )

        result = self.system.get_prop('key1')

        self.assertDictEqual(result, payload)

    @requests_mock.Mocker()
    def test_update_prop(self, m):
        # TODO API docs say this should be PUT
        # TODO I suspect this is meant to be the create function instead
        payload = {
            "@value": "value1",
            "@key": "key1"
        }

        m.register_uri('POST',
                       self.url,  # + '/key1'
                       )

        result = self.system.update_prop(key='key1', value='value1')

        self.assertDictEqual(m.last_request.json(), payload)

    @requests_mock.Mocker()
    def test_delete_prop(self, m):
        m.register_uri('DELETE',
                       self.url + '/key1',
                       )

        result = self.system.delete_prop('key1')

        self.assertTrue(result)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_get_concurrent_sessions(self, m):
        payload = {
            "localSessions": 123,
            "clusterSessions": 123
        }

        m.register_uri('GET',
                       self.host + '/plugins/restapi/v1/system/statistics/sessions',
                       text=json.dumps(payload)
                       )

        result = self.system.get_concurrent_sessions()

        self.assertDictEqual(result, payload)
