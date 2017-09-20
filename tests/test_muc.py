# -*- coding: utf-8 -*-
import requests_mock
import json
from unittest import TestCase
from ofrestapi import muc


class SessionsTestCase(TestCase):
    host = 'http://localhost'
    endpoint = '/plugins/restapi/v1/chatrooms'

    @property
    def url(self):
        return self.host + self.endpoint

    def setUp(self):
        self.muc = muc.Muc(self.host, '1234')

    @requests_mock.Mocker()
    def test_get_room(self, m):
        payload = {
            'roomName': 'roomname',
            'naturalName': 'name',
            'description': 'description',
            'subject': 'subject',
            'password': 'password',
            'maxUsers': 150,
            'persistent': True,
            'publicRoom': True,
            'registrationEnabled': True,
            'canAnyoneDiscoverJID': True,
            'canOccupantsChangeSubject': False,
            'canOccupantsInvite': False,
            'canChangeNickname': True,
            'logEnabled': True,
            'loginRestrictedToNickname': False,
            'membersOnly': False,
            'moderated': False,
            'broadcastPresenceRoles': {'broadcastPresenceRole': ['broadcastroles']},
            'owners': {'owner': ['owners']},
            'admins': {'admin': ['admins']},
            'members': {'member': ['members']},
            'outcasts': {'outcast': ['outcasts']},
        }

        m.register_uri('GET',
                       self.url + '/roomname',
                       text=json.dumps(payload)
                       )

        result = self.muc.get_room('roomname')

        self.assertDictEqual(result, payload)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_get_rooms(self, m):
        payload = {
            "mucRooms": [{
                'roomName': 'roomname',
                'naturalName': 'name',
                'description': 'description',
                'subject': 'subject',
                'password': 'password',
                'maxUsers': 150,
                'persistent': True,
                'publicRoom': True,
                'registrationEnabled': True,
                'canAnyoneDiscoverJID': True,
                'canOccupantsChangeSubject': False,
                'canOccupantsInvite': False,
                'canChangeNickname': True,
                'logEnabled': True,
                'loginRestrictedToNickname': False,
                'membersOnly': False,
                'moderated': False,
                'broadcastPresenceRoles': {'broadcastPresenceRole': ['broadcastroles']},
                'owners': {'owner': ['owners']},
                'admins': {'admin': ['admins']},
                'members': {'member': ['members']},
                'outcasts': {'outcast': ['outcasts']},
            }]
        }

        m.register_uri('GET',
                       self.url,
                       text=json.dumps(payload)
                       )

        result = self.muc.get_rooms()

        self.assertDictEqual(result, payload)

    @requests_mock.Mocker()
    def test_get_room_users(self, m):
        payload = {
            'participants': [{
                'role': 'aeiou',
                'jid': 'aeiou',
                'affiliation': 'aeiou'
            }]
        }

        m.register_uri('GET',
                       self.url + '/roomname/participants',
                       text=json.dumps(payload)
                       )

        result = self.muc.get_room_users('roomname')

        self.assertDictEqual(result, payload)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_add_room(self, m):
        payload = {
            'roomName': 'roomname',
            'naturalName': 'name',
            'description': 'description',
            'subject': 'subject',
            'password': 'password',
            'maxUsers': 150,
            'persistent': True,
            'publicRoom': True,
            'registrationEnabled': True,
            'canAnyoneDiscoverJID': True,
            'canOccupantsChangeSubject': False,
            'canOccupantsInvite': False,
            'canChangeNickname': True,
            'logEnabled': True,
            'loginRestrictedToNickname': False,
            'membersOnly': False,
            'moderated': False,
            'broadcastPresenceRoles': {'broadcastPresenceRole': ['broadcastroles']},
            'owners': {'owner': ['owners']},
            'admins': {'admin': ['admins']},
            'members': {'member': ['members']},
            'outcasts': {'outcast': ['outcasts']},
        }

        m.register_uri('POST',
                       self.url,
                       text=json.dumps(payload),
                       status_code=201
                       )

        result = self.muc.add_room(
            roomname='roomname', name='name', description='description', servicename='conference',
            subject='subject', password='password', maxusers=150, persistent=True,
            public=True, registration=True, visiblejids=True, changesubject=False,
            anycaninvite=False, changenickname=True, logenabled=True,
            registerednickname=False, membersonly=False, moderated=False,
            broadcastroles=['broadcastroles'], owners=['owners'], admins=['admins'],
            members=['members'], outcasts=['outcasts']
        )

        self.assertDictEqual(result, payload)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_delete_room(self, m):
        m.register_uri('DELETE',
                       self.url + '/roomname',
                       )

        result = self.muc.delete_room('roomname')

        self.assertTrue(result)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_update_room(self, m):
        payload = {
            'roomName': 'roomname',
            'naturalName': 'name',
            'description': 'description',
            'subject': 'subject',
            'password': 'password',
            'maxUsers': 150,
            'persistent': True,
            'publicRoom': True,
            'registrationEnabled': True,
            'canAnyoneDiscoverJID': True,
            'canOccupantsChangeSubject': False,
            'canOccupantsInvite': False,
            'canChangeNickname': True,
            'logEnabled': True,
            'loginRestrictedToNickname': False,
            'membersOnly': False,
            'moderated': False,
            'broadcastPresenceRoles': {'broadcastPresenceRole': ['broadcastroles']},
            'owners': {'owner': ['owners']},
            'admins': {'admin': ['admins']},
            'members': {'member': ['members']},
            'outcasts': {'outcast': ['outcasts']},
        }

        m.register_uri('PUT',
                       self.url + '/roomname'
                       )

        result = self.muc.update_room(
            roomname='roomname', name='name', description='description', servicename='conference',
            subject='subject', password='password', maxusers=150, persistent=True,
            public=True, registration=True, visiblejids=True, changesubject=False,
            anycaninvite=False, changenickname=True, logenabled=True,
            registerednickname=False, membersonly=False, moderated=False,
            broadcastroles=['broadcastroles'], owners=['owners'], admins=['admins'],
            members=['members'], outcasts=['outcasts']
        )

        self.assertDictEqual(m.last_request.json(), payload)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_grant_user_role(self, m):
        m.register_uri('POST',
                       self.url + '/roomname/owner/jim',
                       )

        result = self.muc.grant_user_role('roomname', 'jim', 'owner')

        self.assertTrue(result)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')

    @requests_mock.Mocker()
    def test_revoke_user_role(self, m):
        m.register_uri('DELETE',
                       self.url + '/roomname/owner/jim',
                       )

        result = self.muc.revoke_user_role('roomname', 'jim', 'owner')

        self.assertTrue(result)
        self.assertEqual(m.last_request.qs['servicename'][0], 'conference')
