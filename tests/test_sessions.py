# -*- coding: utf-8 -*-
import requests_mock
import json
from unittest import TestCase
from ofrestapi import sessions


class SessionsTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/sessions'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.sessions = sessions.Sessions(self.host, '1234')

    @requests_mock.Mocker()
    def test_get_sessions(self, m):
        payload = {
            'sessions': [{
                'hostName': 'aeiou',
                'sessionStatus': 'aeiou',
                'lastActionDate': '{}',
                'sessionId': 'aeiou',
                'creationDate': '{}',
                'priority': 123,
                'secure': True,
                'node': 'aeiou',
                'resource': 'aeiou',
                'presenceMessage': 'aeiou',
                'hostAddress': 'aeiou',
                'presenceStatus': 'aeiou',
                'username': 'aeiou'
            }]
        }

        m.register_uri('GET',
                       self.url,
                       text=json.dumps(payload)
                       )

        result = self.sessions.get_sessions()

        self.assertDictEqual(result, payload)

    @requests_mock.Mocker()
    def test_get_user_sessions(self, m):
        payload = {
            'hostName': 'aeiou',
            'sessionStatus': 'aeiou',
            'lastActionDate': '{}',
            'sessionId': 'aeiou',
            'creationDate': '{}',
            'priority': 123,
            'secure': True,
            'node': 'aeiou',
            'resource': 'aeiou',
            'presenceMessage': 'aeiou',
            'hostAddress': 'aeiou',
            'presenceStatus': 'aeiou',
            'username': 'aeiou'
        }

        m.register_uri('GET',
                       self.url + '/aeiou',
                       text=json.dumps(payload)
                       )

        result = self.sessions.get_user_sessions('aeiou')

        self.assertDictEqual(result, payload)
        
    @requests_mock.Mocker()
    def test_close_user_sessions(self, m):
        m.register_uri('DELETE',
                       self.url + '/aeiou',
                       )

        result = self.sessions.close_user_sessions('aeiou')

        self.assertTrue(result)
