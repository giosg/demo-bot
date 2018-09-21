# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from server.bot import ChatBot
from responses import RequestsMock
import unittest
import json

responses = RequestsMock(assert_all_requests_are_fired=True)


class BotTest(unittest.TestCase):

    longMessage = True
    maxDiff = None

    def setUp(self):
        responses.reset()
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
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/rooms/room1', json={'language_code': 'en'})
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1', json={
            'present_user_participant_count': 0,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({'id': 'chat1', 'room_id': 'room1'})
        req0, req1, req2, req3, req4, req5 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients/client1')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1')

        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        self.assertEqual(json.loads(req4.request.body), {"is_participating": True, "composing_status": "idle"})

        self.assertEqual(req5.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req5.request.body), {
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
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/rooms/room1', json={'language_code': 'en'})
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1', json={
            'present_user_participant_count': 0,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({'id': 'chat1', 'room_id': 'room1'})
        req0, req1, req2, req3, req4, req5 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1')

        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        self.assertEqual(json.loads(req4.request.body), {"is_participating": True, "composing_status": "idle"})

        self.assertEqual(req5.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')

    @responses.activate
    def test_handle_new_routed_chat_with_present_user_participants(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1', json={
            'present_user_participant_count': 1,
        })
        self.bot.handle_new_routed_chat({'id': 'chat1', 'room_id': 'room1'})
        req0, req1, req2, req3 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1')

    @responses.activate
    def test_handle_new_visitor_chat_message(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'msg',
            'sender_type': 'visitor',
            'response_value': None,
        })
        req0, req1, req2, req3, req4 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req4.request.body), {
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

    @responses.activate
    def test_handle_new_visitor_chat_message_if_visitor_has_requested_human(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages', json={'results': [{'response_value': 'request_human'}], 'next': None})
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'msg',
            'sender_type': 'visitor',
            'response_value': None,
        })
        req0, req1, req2, req3 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')

    @responses.activate
    def test_handle_visitor_clicks_on_customer_service_agent_link(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "https://www.giosg.com/support/user",
        })
        req0, req1, req2, req3 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req3.request.body), {
            "message": "From this page you can find information that customer service agents would like helpful!",
            "attachments": [{
                "text": "Any other topic in which I could help you?",
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
    def test_handle_visitor_clicks_on_manager_user_link(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "https://www.giosg.com/support/manager",
        })
        req0, req1, req2, req3 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req3.request.body), {
            "message": "From this page you can find information helpful for manager users!",
            "attachments": [{
                "text": "Any other topic in which I could help you?",
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
    def test_handle_visitor_clicks_on_developer_link(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "https://www.giosg.com/support/developer",
        })
        req0, req1, req2, req3 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})
        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req3.request.body), {
            "message": "Oh, you are a developer! I'm also been created by a developer! Here's some nerdy information for you!",
            "attachments": [{
                "text": "Any other topic in which I could help you?",
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
    def test_handle_visitor_requests_human_with_online_team(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/orgs/org1/teams', json={
            'results': [{
                'id': 'team1',
                'name': "Customer service",
                'is_online': True,
            }],
            'next': None,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/outgoing_chat_invitations')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "request_human",
        })
        req0, req1, req2, req3, req4, req5, req6, req7 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/orgs/org1/teams')

        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req4.request.body), {
            "message": "Cool! I'll invite my fellow human co-worker to this chat!",
        })

        self.assertEqual(req5.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/outgoing_chat_invitations')
        self.assertEqual(json.loads(req5.request.body), {
            "invited_team_id": "team1",
        })

        self.assertEqual(req6.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req6.request.body), {
            "message": "They will join in a moment and I'll leave you guys!",
        })

        self.assertEqual(req7.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req7.request.body), {
            "message": "But before I go, could you please tell me if you found this information helpful?",
            "attachments": [{
                "actions": [{
                    "text": "Yes",
                    "type": "button",
                    "value": "positive_feedback",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": False
                }, {
                    "text": "No",
                    "type": "button",
                    "value": "negative_feedback",
                    "style": "brand_secondary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": False
                }]
            }],
        })

    @responses.activate
    def test_handle_visitor_requests_human_with_online_team_for_finnish_team(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/rooms/room1', json={'language_code': 'fi'})
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/orgs/org1/teams', json={
            'results': [{
                'id': 'team1',
                'name': "Customer service (FI)",
                'is_online': True,
            }],
            'next': None,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/outgoing_chat_invitations')
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "request_human",
        })
        req0, req1, req2, req3, req4, req5, req6, req7 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/orgs/org1/teams')

        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req4.request.body), {
            "message": "Oukkidoukki! Kutsun ihmiskollegani tähän chattiin!",
        })

        self.assertEqual(req5.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/outgoing_chat_invitations')
        self.assertEqual(json.loads(req5.request.body), {
            "invited_team_id": "team1",
        })

        self.assertEqual(req6.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req6.request.body), {
            "message": "Hän liittyy tuossa tuokiossa ja jätän teidät kahden!",
        })

        self.assertEqual(req7.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req7.request.body), {
            "message": "Voisinko kuitenkin ensin kysyä, että oliko tarjoamani tiedot teidän mielestänne hyödyllisiä?",
            "attachments": [{
                "actions": [{
                    "text": "Kyllä",
                    "type": "button",
                    "value": "positive_feedback",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": False
                }, {
                    "text": "Ei",
                    "type": "button",
                    "value": "negative_feedback",
                    "style": "brand_secondary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": False
                }]
            }],
        })

    @responses.activate
    def test_handle_visitor_requests_human_with_offline_team(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/orgs/org1/teams', json={
            'results': [{
                'id': 'team1',
                'name': "Customer service",
                'is_online': False,
            }],
            'next': None,
        })
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'action',
            'sender_type': 'visitor',
            'response_value': "request_human",
        })
        req0, req1, req2, req3, req4 = responses.calls
        self.assertEqual(req0.request.url, 'https://service.giosg.com/api/v5/users/user1/rooms/room1')

        self.assertEqual(req1.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')

        self.assertEqual(req2.request.url, 'https://service.giosg.com/api/v5/users/user1/clients')
        self.assertEqual(req2.request.method, 'POST')
        self.assertEqual(json.loads(req2.request.body), {"presence_expires_in": 7200})

        self.assertEqual(req3.request.url, 'https://service.giosg.com/api/v5/orgs/org1/teams')

        self.assertEqual(req4.request.url, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.assertEqual(json.loads(req4.request.body), {
            "message": "Oh, sorry but could not find online customer service agents! They might have just left for a cup of coffee or something!",
            "attachments": [{
                "text": "You can also contact us by email: [support@giosg.com](mailto:support@giosg.com)",
            }],
        })

    @responses.activate
    def test_ignore_new_join_chat_messages(self):
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'join',
            'sender_type': 'visitor',
            'response_value': None,
        })
        self.assertEqual(list(responses.calls), [])

    @responses.activate
    def test_ignore_new_leave_chat_messages(self):
        self.bot.handle_new_user_chat_message({
            'id': 'message1',
            'room_id': 'room1',
            'chat_id': 'chat1',
            'type': 'leave',
            'sender_type': 'visitor',
            'response_value': None,
        })
        self.assertEqual(list(responses.calls), [])

    @responses.activate
    def test_defaults_to_english_with_unsupported_language_code(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/rooms/room1', json={'language_code': 'es'})
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1', json={
            'present_user_participant_count': 0,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({'id': 'chat1', 'room_id': 'room1'})
        req = responses.calls[-1]
        self.assertEqual(json.loads(req.request.body), {
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
    def test_support_finnish_language(self):
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/clients', json={'results': [], 'next': None})
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/clients')
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/rooms/room1', json={'language_code': 'fi'})
        responses.add(responses.GET, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1', json={
            'present_user_participant_count': 0,
        })
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/routed_chats/chat1/memberships')
        responses.add(responses.POST, 'https://service.giosg.com/api/v5/users/user1/chats/chat1/messages')
        self.bot.handle_new_routed_chat({'id': 'chat1', 'room_id': 'room1'})
        req = responses.calls[-1]
        self.assertEqual(json.loads(req.request.body), {
            "message": "Olen esimerkki-chatbotti! Kuinka voisin olla teidän avuksenne?",
            "attachments": [{
                "text": "Valitsisitko alta roolinne:",
                "actions": [{
                    "text": "Asiakaspalvelija",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/user",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Pääkäyttäjä",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/manager",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Sovelluskehittäjä",
                    "type": "link_button",
                    "link_target": "_parent",
                    "value": "https://www.giosg.com/support/developer",
                    "style": "brand_primary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }, {
                    "text": "Ohjaa minut ihmiselle",
                    "type": "button",
                    "value": "request_human",
                    "style": "brand_secondary",
                    "is_disabled_on_selection": True,
                    "is_disabled_on_visitor_message": True
                }]
            }],
        })
