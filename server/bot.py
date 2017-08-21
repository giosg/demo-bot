# -*- coding: utf-8 -*-


class ChatBot(object):

    # Handlers
    def handle_feedback(self):
        return {"message": "Thank you for participating our feedback survey."}

    # Getters
    def get_feedback(self):
        actions = [
            {
                "text": "Yes",
                "type": "button",
                "value": "yes",
                "style": "success",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "I don't know",
                "type": "button",
                "value": "maybe",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "No",
                "type": "button",
                "value": "no",
                "style": "danger",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            }
        ]
        attachments = [{
            "text": "Was this conversation helpful?",
            "actions": actions
        }]
        message = {"message": "We would like to hear your feedback about this conversation", "attachments": attachments}
        return message

    def get_numeric_feedback(self):
        actions = [
            {
                "text": "1",
                "type": "button",
                "value": "1",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "2",
                "type": "button",
                "value": "2",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "3",
                "type": "button",
                "value": "3",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "4",
                "type": "button",
                "value": "4",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
            {
                "text": "5",
                "type": "button",
                "value": "5",
                "style": "info",
                "is_disabled_on_selection": True,
                "is_disabled_on_visitor_message": False
            },
        ]
        attachments = [{
            "text": "From 1 to 5, how would you rate this conversation?",
            "actions": actions
        }]
        message = {"message": "We would like to hear your feedback about this conversation.", "attachments": attachments}
        return message
