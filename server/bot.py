# -*- coding: utf-8 -*-

from conf import SERVICE_URL
from retry_session import retry_session


class ChatBot(object):
    """
    Bot implementation which contains all functionality e.g.
    sending new chat message or updating presence in giosg system.
    """
    def __init__(self):
        # Initialize session and try to retry twice.
        self.session = retry_session(2)

    def update_or_create_user_client(self, user_id):
        # Get existing user client if one
        response = self.session.get('https://{}/api/v5/users/{}/clients'.format(SERVICE_URL, user_id))

        # If existing user client was found, update it otherwise create new
        pass

    def is_allowed_to_join(self, user_id, chat_id):
        pass

    def join_to_chat(self, user_id, chat_id):
        pass

    def send_welcoming_message(self, user_id, chat_id):
        """
        Format welcoming message and makes API request
        """
        actions = [
            {
                "text": "Customer service agent",
                "type": "link_button",
                "link_target": "_parent",
                "value": "https://www.giosg.com/support/user",
                "style": "brand_primary",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "Manager user",
                "type": "link_button",
                "link_target": "_parent",
                "value": "https://www.giosg.com/support/manager",
                "style": "brand_primary",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "Developer",
                "type": "link_button",
                "link_target": "_parent",
                "value": "https://www.giosg.com/support/developer",
                "style": "brand_primary",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            }
        ]
        attachments = [{
            "text": "are you:",
            "actions": actions
        }]
        message = {"message": "Welcome to giosg's support side,", "attachments": attachments}
        return message

    def handle_visitor_message(self, user_id):
        pass

    def send_feedback_message(self, user_id, chat_id):
        pass

    def check_assigned_team_online_status(organization_id):
        pass

    def invite_assigned_team_to_chat(self, user_id, chat_id):
        pass

    def leave_leadform_helpers(self, user_id, chat_id):
        pass

    def send_farewell_messages(self, user_id, chat_id):
        pass

    def leave_chat_conversation(self, user_id, chat_id):
        pass
