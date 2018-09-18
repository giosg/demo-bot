# -*- coding: utf-8 -*-
from conf import INVITEE_TEAM_NAME
from giosg import APIClient


class ChatBot(object):
    """
    Bot implementation which contains all functionality e.g.
    sending new chat message or updating presence in giosg system.
    """
    def __init__(self, auth):
        self.api = APIClient(auth)
        self.auth = auth

    def update_or_create_user_client(self):
        # Get existing user client if one
        user_clients = self.api.list('/api/v5/users/{user_id}/clients'.format(**self.auth))
        if user_clients:
            client_id = user_clients[0]['id']
            self.api.update(
                url='/api/v5/users/{user_id}/clients/{client_id}'.format(client_id=client_id, **self.auth),
                payload={
                    'presence_expires_in': 60,
                },
            )
        else:
            self.api.create(
                url='/api/v5/users/{user_id}/clients'.format(**self.auth),
                payload={
                    'presence_expires_in': 60,
                },
            )

    def is_allowed_to_join(self, chat_id):
        chat = self.api.retrieve(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}'.format(chat_id=chat_id, **self.auth),
        )
        return chat['present_user_participant_count'] == 0

    def join_to_chat(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}/memberships'.format(chat_id=chat_id, **self.auth),
            payload={
                'is_participating': True,
                'composing_status': 'idle',
            },
        )

    def send_welcoming_message(self, chat_id):
        """
        Format welcoming message and makes API request
        """
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Welcome to giosg's support side,",
                "attachments": [{
                    "text": "are you:",
                    "actions": [{
                        "text": "Customer service agent",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/user",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Manager user",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/manager",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Developer",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/developer",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }]
                }],
            },
        )

    def react_to_customer_service_agent(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Here's some information for customer service agents!",
                "attachments": [{
                    "text": "Any other topic in which I could help you?",
                    "actions": [{
                        "text": "Manager user",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/manager",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Developer",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/developer",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Let me chat with a human",
                        "type": "button",
                        "value": "request_human",
                        "style": "brand_secondary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }]
                }],
            },
        )

    def react_to_manager_user(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Here's some information that is helpful for manager users!",
                "attachments": [{
                    "text": "Any other topic in which I could help you?",
                    "actions": [{
                        "text": "Customer service agent",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/user",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Developer",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/developer",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Let me chat with a human",
                        "type": "button",
                        "value": "request_human",
                        "style": "brand_secondary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }]
                }],
            },
        )

    def react_to_developer(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Oh, you are a developer! I'm also been created by a developer! Here's some nerdy information for you!",
                "attachments": [{
                    "text": "Any other topic in which I could help you?",
                    "actions": [{
                        "text": "Manager user",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/manager",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Customer service agent",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/user",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Let me chat with a human",
                        "type": "button",
                        "value": "request_human",
                        "style": "brand_secondary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": False
                    }]
                }],
            },
        )

    def react_to_request_human(self, chat_id):
        online_team = self.api.search(
            '/api/v5/orgs/{organization_id}/teams'.format(**self.auth),
            lambda team: team['is_online'] and team['name'].lower() == INVITEE_TEAM_NAME.lower()
        )
        if online_team:
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/outgoing_chat_invitations'.format(chat_id=chat_id, **self.auth),
                payload={
                    "invited_team_id": online_team['id'],
                },
            )
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": "OK, I invited my fellow human co-worker to this chat! They will join in a moment and I'll leave you guys!",
                },
            )
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": "But before I go, could you tell me if you found this information helpful?",
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
                },
            )
        else:
            # Did not find an online team to invite to this chat
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": "Oh, sorry but could not find online customer service agents! They might have just left!",
                    "attachments": [{
                        "text": "Maybe you could [send them email](mailto:support@giosg.com) instead?",
                    }],
                },
            )

    def react_to_positive_feedback(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Good to hear that! My human fellow will continue chatting with you!",
            },
        )
        self.leave_chat_conversation(chat_id)

    def react_to_negative_feedback(self, chat_id):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": "Sorry to hear that! I hope that my human fellow can serve you better!",
            },
        )
        self.leave_chat_conversation(chat_id)

    def handle_visitor_message(self, chat_id):
        pass

    def leave_chat_conversation(self, chat_id):
        self.api.update(
            url='/api/v5/users/{user_id}/chat_memberships/{chat_id}'.format(chat_id=chat_id, **self.auth),
            payload={
                "is_participating": False,
            },
        )
