# -*- coding: utf-8 -*-
import requests_mock
import json
from unittest import TestCase
from ofrestapi import messages


class MessagesTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/messages/users'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.messages = messages.Messages(self.host, '1234')

    @requests_mock.Mocker()
    def test_send_broadcast(self, m):
        payload = {
            'body': 'Hello world!',
        }

        m.register_uri('POST',
                       self.url,
                       status_code=201,
                       )

        self.messages.send_broadcast('Hello world!')

        self.assertTrue(m.called)
        self.assertDictEqual(m.last_request.json(), payload)

    @requests_mock.Mocker()
    def test_get_unread_messages(self, m):
        payload = {
            "jid": "sally@example.com",
            "count": 123
        }

        m.register_uri('GET',
                       self.host + '/plugins/restapi/v1/archive/messages/unread/' + 'sally@example.com',
                       text=json.dumps(payload)
                       )

        response = self.messages.get_unread_messages('sally@example.com')

        self.assertTrue(m.called)
        self.assertDictEqual(response, payload)

