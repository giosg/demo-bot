# -*- coding: utf-8 -*-
"""
Functional logic for the chatbot.
"""
from __future__ import unicode_literals
from conf import INVITEE_TEAM_NAMES
from giosg import APIClient
from languages import load_translations_for_language


# How long the bot should keep themselves "present" in Giosg system during inactivity
BOT_PRSENECE_DURATION = 7200  # = 2 hours


class ChatBot(object):
    """
    Bot implementation which contains all functionality e.g.
    sending new chat message or updating presence in giosg system.
    """
    def __init__(self, auth):
        self.api = APIClient(auth)
        self.auth = auth

    ######################################
    # Handlers for webhook notifications #
    ######################################

    def handle_new_routed_chat(self, chat):
        """
        Handles a new chat that has been routed to the bot.
        This is called when receiving a webhook notification about a new routed chat:

        /api/v5/users/{user_id}/routed_chats
        """
        chat_id = chat['id']
        room_id = chat['room_id']
        language_code = self.get_language_code_for_room(room_id)
        translations = load_translations_for_language(language_code)
        self.make_present()
        if self.is_allowed_to_join(chat_id):
            self.join_chat(chat_id)
            self.send_option_links(chat_id, 'hello_text', 'hello_hint', translations)
            self.send_option_link_to_chat_with_human(chat_id, 'visitor_message_response_text_request_human', 'visitor_message_response_hint_request_human', translations)

    def handle_new_user_chat_message(self, message):
        """
        Handles a new chat message that has been added to any of the chats
        to which the user has been routed. This is called when receiving a webhook
        notification about a new chat message:

        /api/v5/users/{user_id}/chats/*/messages
        """
        chat_id = message['chat_id']
        room_id = message['room_id']
        message_type = message['type']
        sender_type = message['sender_type']
        response_value = message['response_value']

        # Only react to messages from a visitor, not from this bot or users
        # Also, ignore all other message types actual messages ('msg') and actions ('action')
        if sender_type == 'user' or message_type not in ('msg', 'action'):
            return

        language_code = self.get_language_code_for_room(room_id)
        translations = load_translations_for_language(language_code)
        invitee_team_name = INVITEE_TEAM_NAMES[language_code]
        self.make_present()

        if message['type'] == 'msg':
            self.react_to_visitor_message(chat_id, translations)
        elif response_value == 'request_human':
            self.react_to_request_human(chat_id, invitee_team_name, translations)
        elif response_value == 'positive_feedback':
            self.react_to_positive_feedback(chat_id, translations)
        elif response_value == 'negative_feedback':
            self.react_to_negative_feedback(chat_id, translations)
        elif response_value == "https://www.giosg.com/support/user":
            self.react_to_customer_service_agent(chat_id, translations)
        elif response_value == "https://www.giosg.com/support/manager":
            self.react_to_manager_user(chat_id, translations)
        elif response_value == "https://www.giosg.com/support/developer":
            self.react_to_developer(chat_id, translations)

    #######################################################
    # Internal helper functions for the bot functionality #
    #######################################################

    def make_present(self):
        """
        Ensures that the bot user is in "present" state in the Giosg system
        for the next two (2) hours.
        """
        # List all the user clients for this bot
        user_clients = self.api.list('/api/v5/users/{user_id}/clients'.format(**self.auth))
        if user_clients:
            # If there is an existing user client, then update it
            client_id = user_clients[0]['id']
            self.api.update(
                url='/api/v5/users/{user_id}/clients/{client_id}'.format(client_id=client_id, **self.auth),
                payload={
                    'presence_expires_in': BOT_PRSENECE_DURATION,
                },
            )
        else:
            # There is no existing user client yet, so create a new
            self.api.create(
                url='/api/v5/users/{user_id}/clients'.format(**self.auth),
                payload={
                    'presence_expires_in': BOT_PRSENECE_DURATION,
                },
            )

    def is_allowed_to_join(self, chat_id):
        chat = self.api.retrieve(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}'.format(chat_id=chat_id, **self.auth),
        )
        return chat['present_user_participant_count'] == 0

    def join_chat(self, chat_id):
        """
        Ensures that the bot user is a member of the given chat and participating in it,
        so that it can send chat messages to it.
        """
        self.api.create(
            url='/api/v5/users/{user_id}/routed_chats/{chat_id}/memberships'.format(chat_id=chat_id, **self.auth),
            payload={
                'is_participating': True,
                'composing_status': 'idle',
            },
        )

    def send_option_links(self, chat_id, message_key, hint_key, translations):
        """
        Sends a message with a set of buttons that the visitor can click in the chat window.
        """
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": translations[message_key],
                "attachments": [{
                    "text": translations[hint_key],
                    "actions": [{
                        "text": translations["button_text_customer_service_agent"],
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/user",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": True
                    }, {
                        "text": translations["button_text_manager_user"],
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/manager",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": True
                    }, {
                        "text": translations["button_text_developer"],
                        "type": "link_button",
                        "link_target": "_parent",
                        "value": "https://www.giosg.com/support/developer",
                        "style": "brand_primary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": True
                    }]
                }],
            },
        )

    def send_option_link_to_chat_with_human(self, chat_id, message_key, hint_key, translations):
        """
        Sends a message with a set of buttons that the visitor can click in the chat window.
        """
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": translations[message_key],
                "attachments": [{
                    "text": translations[hint_key],
                    "actions": [{
                        "text": translations["button_text_request_human"],
                        "type": "button",
                        "value": "request_human",
                        "style": "brand_secondary",
                        "is_disabled_on_selection": True,
                        "is_disabled_on_visitor_message": True
                    }]
                }],
            },
        )

    def react_to_visitor_message(self, chat_id, translations):
        # Check if visitor has already requested human
        has_requested_human = self.api.search(
            '/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            lambda message: message['response_value'] == 'request_human'
        )
        if not has_requested_human:
            self.send_option_links(chat_id, 'visitor_message_response_text', 'visitor_message_response_hint', translations)
            self.send_option_link_to_chat_with_human(chat_id, 'visitor_message_response_text_request_human', 'visitor_message_response_hint_request_human', translations)

    def react_to_customer_service_agent(self, chat_id, translations):
        self.send_option_links(chat_id, 'customer_service_agent_message', 'customer_service_agent_hint', translations)
        self.send_option_link_to_chat_with_human(chat_id, 'visitor_message_response_text_request_human', 'visitor_message_response_hint_request_human', translations)

    def react_to_manager_user(self, chat_id, translations):
        self.send_option_links(chat_id, 'manager_user_message', 'manager_user_hint', translations)
        self.send_option_link_to_chat_with_human(chat_id, 'visitor_message_response_text_request_human', 'visitor_message_response_hint_request_human', translations)

    def react_to_developer(self, chat_id, translations):
        self.send_option_links(chat_id, 'developer_message', 'developer_hint', translations)
        self.send_option_link_to_chat_with_human(chat_id, 'visitor_message_response_text_request_human', 'visitor_message_response_hint_request_human', translations)

    def react_to_request_human(self, chat_id, invitee_team_name, translations):
        # Find the team by the configured name (case-insensitive) if there is one currently online
        online_team = self.api.search(
            '/api/v5/orgs/{organization_id}/teams'.format(**self.auth),
            lambda team: team['is_online'] and team['name'].lower() == invitee_team_name.lower()
        )
        if online_team:
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": translations['request_human_text'],
                },
            )
            # Invite the team to this chat
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/outgoing_chat_invitations'.format(chat_id=chat_id, **self.auth),
                payload={
                    "invited_team_id": online_team['id'],
                },
            )
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": translations["request_human_invite_text"],
                },
            )
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": translations['feedback_text'],
                    "attachments": [{
                        "actions": [{
                            "text": translations['feedback_yes'],
                            "type": "button",
                            "value": "positive_feedback",
                            "style": "brand_primary",
                            "is_disabled_on_selection": True,
                            "is_disabled_on_visitor_message": False
                        }, {
                            "text": translations['feedback_no'],
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
            # Did not find an online team to invite to this chat => apologize the visitor
            self.api.create(
                url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
                payload={
                    "message": translations['team_offline_text'],
                    "attachments": [{
                        "text": translations['team_offline_hint'],
                    }],
                },
            )

    def react_to_positive_feedback(self, chat_id, translations):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": translations['positive_feedback_response_text'],
            },
        )
        self.leave_chat_conversation(chat_id)

    def react_to_negative_feedback(self, chat_id, translations):
        self.api.create(
            url='/api/v5/users/{user_id}/chats/{chat_id}/messages'.format(chat_id=chat_id, **self.auth),
            payload={
                "message": translations['negative_feedback_response_text'],
            },
        )
        self.leave_chat_conversation(chat_id)

    def leave_chat_conversation(self, chat_id):
        # Switches the chat membership to non-participating state
        self.api.update(
            url='/api/v5/users/{user_id}/chat_memberships/{chat_id}'.format(chat_id=chat_id, **self.auth),
            payload={
                "is_participating": False,
            },
        )

    def get_language_code_for_room(self, room_id):
        """
        Retrieves details about the given room, and returns the language code
        """
        try:
            room = self.api.retrieve('/api/v5/users/{user_id}/rooms/{room_id}'.format(room_id=room_id, **self.auth))
            language_code = room['language_code']
        except Exception:
            # Could not determine the room language. Instead of failing, let's default to English
            language_code = 'en'
        else:
            # If language code is not supported, then default to English
            if language_code not in ('fi', 'en'):
                language_code = 'en'
        return language_code
