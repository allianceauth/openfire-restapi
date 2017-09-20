# -*- coding: utf-8 -*-
import requests_mock
import requests
import json
from unittest import TestCase
from ofrestapi import exception, groups


class GroupsTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/groups'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.groups = groups.Groups(self.host, '1234')

    @requests_mock.Mocker()
    def test_get_groups(self, m):
        payload = [
            {
                'name': 'my group',
                'description': 'Its a group',
            },
        ]
        m.register_uri('GET',
                       self.url,
                       text=json.dumps(payload)
                       )

        result = self.groups.get_groups()

        self.assertListEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_get_group(self, m):
        payload = {
                'name': 'My Group',
                'description': 'Its a group',
        }
        m.register_uri('GET',
                       self.url + '/my%20group',
                       text=json.dumps(payload)
                       )

        result = self.groups.get_group('my group')

        self.assertDictEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_add_group(self, m):
        m.register_uri('POST',
                       self.url,
                       status_code=201,
                       )

        result = self.groups.add_group('my group', 'Its a group')

        self.assertIs(type(result), bool)
        self.assertTrue(result)
        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), {
            'name': 'my group',
            'description': 'Its a group',
        })

    @requests_mock.Mocker()
    def test_delete_group(self, m):
        m.register_uri('DELETE',
                       self.url + '/my%20group',
                       status_code=200,
                       )

        result = self.groups.delete_group('my group')

        self.assertIs(type(result), bool)
        self.assertTrue(result)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_update_group(self, m):
        m.register_uri('PUT',
                       self.url + '/my%20group',
                       status_code=200,
                       )

        result = self.groups.update_group('my group', 'Its a group')

        self.assertIs(type(result), bool)
        self.assertTrue(result)
        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), {
            'name': 'my group',
            'description': 'Its a group',
        })
