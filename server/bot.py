# -*- coding: utf-8 -*-

from retry_session import retry_session


class ChatBot(object):
    """
    Bot implementation which contains oiqhwg
    """
    def __init__(self):
        # Try to retry twice
        self.session = retry_session(2)

    def update_or_create_user_client(user_id):
        pass

    def is_allowed_to_join(user_id, chat_id):
        pass

    def join_to_chat(user_id, chat_id):
        pass

    def send_welcoming_message(user_id, chat_id):
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

    def handle_visitor_message(user_id):
        pass

    def send_feedback_message(user_id, chat_id):
        pass

    def check_assigned_team_online_status(organization_id):
        pass

    def invite_assigned_team_to_chat(user_id, chat_id):
        pass

    def leave_leadform_helpers(user_id, chat_id):
        pass

    def send_farewell_messages(user_id, chat_id):
        pass

    def leave_chat_conversation(user_id, chat_id):
        pass

    # Handlers
    def handle_welcoming_message(self):
        pass

    def handle_feedback(self):
        return {"message": "Thank you for participating our feedback survey."}
