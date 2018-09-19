# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from server.bot import ChatBot
import responses
import unittest
import json


class BotTest(unittest.TestCase):

    longMessage = True
    maxDiff = None

    def setUp(self):
        self.bot = ChatBot({
            'access_token': '<ACCESS_TOKEN>',
            'token_type': 'Bearer',
            'user_id': 'user1',
            'organization_id': 'org1',
        })

    @responses.activate
    def test_handle_new_routed_chat_with_existing_client(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={
            'results': [{'id': 'client1'}],
            'next': None,
        })
        responses.add(responses.PATCH, 'https://service.giosg.com/api/v5/users/user1/clients/client1')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({
            'id': 'chat1',
        })
        req1, req2, req3, req4 = responses.calls
        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients/client1')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        self.assertEqual(json.loads(req3.request.body), {"is_participating": True, "composing_status": "idle"})
        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req4.request.body), {
            "message": "I'm a simple example chatbot! How may I help you?",
            "attachments": [{
                "text": "Please choose your role below:",
                "actions": [{
                    "text": "Customer service agent",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/user",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Manager user",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/manager",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Developer",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/developer",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Let me chat with a human",
                    "type": "button",
                    "value": "request_human",
                    "style": "brand_secondary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }]
            }],
        })

    @responses.activate
    def test_handle_new_routed_chat_without_existing_client(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={
            'results': [],
            'next': None,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({
            'id': 'chat1',
        })
        req1, req2, req3, req4 = responses.calls
        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        self.assertEqual(json.loads(req3.request.body), {"is_participating": True, "composing_status": "idle"})
        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')

    @responses.activate
    def test_handle_new_visitor_chat_message(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'chat_id': 'chat1',
            'type': 'msg',
            'sender_type': 'visitor',
            'response_value': None,
        })
        req1, req2, req3 = responses.calls
        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req3.request.body), {
            "message": "I apologize, I'm just a simple example bot uncapable of understanding human language! 😅",
            "attachments": [{
                "text": "I only know what to do if you choose one of the options below!",
                "actions": [{
                    "text": "Customer service agent",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/user",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Manager user",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/manager",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Developer",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/developer",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Let me chat with a human",
                    "type": "button",
                    "value": "request_human",
                    "style": "brand_secondary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }]
            }],
        })
