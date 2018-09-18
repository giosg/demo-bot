# -*- coding: utf-8 -*-
import giosg


class ChatBot(object):
    """
    Bot implementation which contains all functionality e.g.
    sending new chat message or updating presence in giosg system.
    """
    def __init__(self, auth):
        self.auth = auth

    def update_or_create_user_client(self):
        # Get existing user client if one
        user_clients = giosg.list(
            url='/api/v5/users/{user_id}/clients'.format(**self.auth),
            auth=self.auth,
        )
        if user_clients:
            client_id = user_clients[0]['id']
            giosg.update(
                url='/api/v5/users/{user_id}/clients/{client_id}'.format(client_id=client_id, **self.auth),
                auth=self.auth,
                payload={
                    'presence_expires_in': 60,
                },
            )
        else:
            giosg.create(
                url='/api/v5/users/{user_id}/clients'.format(**self.auth),
                auth=self.auth,
                payload={
                    'presence_expires_in': 60,
                },
            )

    def is_allowed_to_join(self, chat_id):
        chat = giosg.retrieve(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}'.format(chat_id=chat_id, **self.auth),
            auth=self.auth,
        )
        return chat['present_user_participant_count'] == 0

    def join_to_chat(self, chat_id):
        giosg.create(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}/memberships'.format(chat_id=chat_id, **self.auth),
            auth=self.auth,
            payload={
                'is_participating': True,
                'composing_status': 'idle',
            },
        )

    def send_welcoming_message(self, chat_id):
        """
        Format welcoming message and makes API request
        """
        giosg.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            auth=self.auth,
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
                        "is_disabled_on_selection": False,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Manager user",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/manager",
                        "style": "brand_primary",
                        "is_disabled_on_selection": False,
                        "is_disabled_on_visitor_message": False
                    }, {
                        "text": "Developer",
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/developer",
                        "style": "brand_primary",
                        "is_disabled_on_selection": False,
                        "is_disabled_on_visitor_message": False
                    }]
                }],
            },
        )

    def handle_visitor_message(self, chat_id):
        pass

    def send_feedback_message(self, chat_id):
        pass

    def check_assigned_team_online_status(self):
        pass

    def invite_assigned_team_to_chat(self, chat_id):
        pass

    def send_farewell_messages(self, chat_id):
        pass

    def leave_chat_conversation(self, chat_id):
        pass
