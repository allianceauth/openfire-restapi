# -*- coding: utf-8 -*-
import requests_mock
import requests
import json
from unittest import TestCase
from ofrestapi import exception, users


class UsersTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/users'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.users = users.Users(self.host, '1234')

    @requests_mock.Mocker()
    def test_get_user(self, m):
        payload = {
            'username': 'joe',
            'name': 'Joe Smith',
        }
        m.register_uri('GET',
                       self.url + '/joe',
                       text=json.dumps(payload)
                       )

        result = self.users.get_user('joe')

        self.assertDictEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_get_users(self, m):
        payload = [
            {
                'username': 'joe',
                'name': 'Joe Smith',
            },
            {
                'username': 'sarah',
                'name': 'Sarah Doe',
            }
        ]
        m.register_uri('GET',
                       self.url,
                       text=json.dumps(payload)
                       )

        result = self.users.get_users()

        self.assertListEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_add_user(self, m):
        payload = {
            'username': 'joe',
            'name': 'Joe Smith',
            'password': 'hunter1',
            'email': 'joe.smith@example.com',
            'properties': {
                "property": [
                    {
                        "@key": "prop1",
                        "@value": "val1"
                    },
                ]
            }
        }
        m.register_uri('POST',
                       self.url,
                       status_code=201,
                       text=json.dumps(payload)
                       )

        result = self.users.add_user('joe',
                                     'hunter1',
                                     name='Joe Smith',
                                     email='joe.smith@example.com',
                                     props={
                                         'prop1': 'val1'
                                     })

        self.assertDictEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_update_user(self, m):
        payload = {
            'username': 'jim',
            'name': 'Joe Smith',
            'password': 'hunter1',
            'email': 'joe.smith@example.com',
            'properties': {
                "property": [
                    {
                        "@key": "prop1",
                        "@value": "val1"
                    },
                ]
            }
        }
        m.register_uri('PUT',
                       self.url + '/joe',
                       status_code=201,
                       text=json.dumps(payload)
                       )

        result = self.users.update_user('joe',
                                        newusername='jim',
                                        password='hunter1',
                                        name='Joe Smith',
                                        email='joe.smith@example.com',
                                        props={
                                            'prop1': 'val1'
                                        })

        self.assertTrue(result)
        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), payload)

    @requests_mock.Mocker()
    def test_delete_user(self, m):
        m.register_uri('DELETE',
                       self.url + '/joe',
                       )

        result = self.users.delete_user('joe')

        self.assertTrue(result)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_get_user_groups(self, m):
        payload = [
            {
                'name': 'my group',
                'description': 'Its a group',
            },
        ]
        m.register_uri('GET',
                       self.url + '/joe/groups',
                       text=json.dumps(payload)
                       )

        result = self.users.get_user_groups('joe')

        self.assertListEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_add_user_groups(self, m):
        payload = {
            'groupname': ['my group'],
        }
        m.register_uri('POST',
                       self.url + '/joe/groups',
                       status_code=201,
                       )

        result = self.users.add_user_groups('joe', ['my group'])

        self.assertDictEqual(m.last_request.json(), payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_delete_user_groups(self, m):
        payload = {
            'groupname': ['my group'],
        }
        m.register_uri('DELETE',
                       self.url + '/joe/groups',
                       )

        result = self.users.delete_user_groups('joe', ['my group'])

        self.assertDictEqual(m.last_request.json(), payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_lock_user(self, m):
        m.register_uri('POST',
                       self.host + '/plugins/restapi/v1/lockouts/joe',
                       status_code=201,
                       )

        result = self.users.lock_user('joe')

        self.assertTrue(result)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_lock_user(self, m):
        m.register_uri('DELETE',
                       self.host + '/plugins/restapi/v1/lockouts/joe',
                       )

        result = self.users.unlock_user('joe')

        self.assertTrue(result)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_get_user_roster(self, m):
        payload = [
            {
                'jid': 'sally@example.com/friends',
                'groups': {'group': ['friends']},
            },
        ]
        m.register_uri('GET',
                       self.url + '/joe/roster',
                       text=json.dumps(payload)
                       )

        result = self.users.get_user_roster('joe')

        self.assertListEqual(result, payload)
        self.assertTrue(m.called)

    @requests_mock.Mocker()
    def test_add_user_roster_item(self, m):
        payload = {
            'jid': 'sally@example.com',
            'nickname': 'Sally',
            'subscriptionType': 1,
            'groups': {'group': ['friends']},
        }
        m.register_uri('POST',
                       self.url + '/joe/roster',
                       status_code=201
                       )

        result = self.users.add_user_roster_item('joe',
                                                 'sally@example.com',
                                                 name='Sally',
                                                 subscription=users.Users.SUBSCRIPTION_TO,
                                                 groups=['friends']
                                                 )

        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), payload)

    @requests_mock.Mocker()
    def test_delete_user_roster_item(self, m):

        m.register_uri('DELETE',
                       self.url + '/joe/roster/' + 'sally@example.com',
                       )

        result = self.users.delete_user_roster_item('joe', 'sally@example.com')

        self.assertTrue(m.called)
        self.assertTrue(result)

    @requests_mock.Mocker()
    def test_update_user_roster_item(self, m):
        payload = {
            'jid': 'sally@example.com',
            'nickname': 'Sal',
            'subscriptionType': 3,
            'groups': {'group': ['friends', 'coworkers']},
        }
        m.register_uri('PUT',
                       self.url + '/joe/roster/' + 'sally@example.com',
                       )

        result = self.users.update_user_roster_item('joe',
                                                    'sally@example.com',
                                                    name='Sal',
                                                    subscription=users.Users.SUBSCRIPTION_BOTH,
                                                    groups=['friends', 'coworkers']
                                                    )

        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), payload)
