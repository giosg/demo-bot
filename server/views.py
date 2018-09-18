# -*- coding: utf-8 -*-

from flask import request, abort
from flask_restful import Resource
from bot import ChatBot
from conf import SECRET_STRING


class APIView(Resource):
    """
    API view which contains parsing request data,
    initial request handling, and updating user client.
    Other API views should extend this one.
    """
    def __init__(self):
        # Very low level authentication based on given secret
        if request.args.get('secret') != SECRET_STRING:
            abort(403)

    def post(self):
        # Take needed items from request data as variables
        json_data = request.get_json(force=True)

        # Resource object containing all data changes
        self.resource = json_data.get('resource')
        # Resource ID, this is either the chat ID or message ID
        self.resource_id = json_data.get('resource_id')
        # Authentication object containing user ID and token
        self.authentication = json_data.get('app_user_auth')

        # If resource, resource_id, or authentication
        # data is missing we can't continue
        if not (self.resource or self.authentication or self.resource_id):
            abort(400)

        # Format the data and get needed resources
        # 1. user_id
        # 2. authentication token
        self.user_id = self.authentication.get('user_id')
        self.organization_id = self.authentication.get('organization_id')
        self.token = self.authentication.get('access_token')

        # Initialize chat bot
        self.bot = ChatBot(self.authentication)

        # Update bot's user client or create new user client if none found
        self.bot.update_or_create_user_client()


class ChatAPIView(APIView):
    """
    API view for handling routed chat webhooks.
    In this case the bot has received a notification
    about new chat that has been added.
    """
    def post(self):
        super(ChatAPIView, self).post()

        # When a new chat is routed to the
        # bot, do following steps:
        # 1. There are already some other user participating the chat
        # 2. If not, join to the chat and send the welcoming message
        # allowed_to_join = self.bot.is_allowed_to_join(chat_id=self.resource_id)
        allowed_to_join = True

        # Bot was allowed to join to the chat
        if allowed_to_join:
            self.bot.join_to_chat(chat_id=self.resource_id)
            self.bot.send_welcoming_message(chat_id=self.resource_id)
        return {'detail': 'OK'}


class ChatMessageAPIView(APIView):
    """
    API view for handling routed chat message webhooks.
    In this case the bot has receiver a notification
    about new chat message that has been added.
    """
    def post(self):
        super(ChatMessageAPIView, self).post()
        chat_id = self.resource['chat_id']

        # Only react to messages from a visitor, not from this bot or users
        if self.resource['sender_type'] == 'user':
            return

        response_value = self.resource['response_value']

        if self.resource['type'] != 'action':
            self.bot.handle_visitor_message(chat_id)
        elif response_value == 'request_human':
            self.bot.react_to_request_human(chat_id)
        elif response_value == 'positive_feedback':
            self.bot.react_to_positive_feedback(chat_id)
        elif response_value == 'negative_feedback':
            self.bot.react_to_negative_feedback(chat_id)
        elif response_value == "https://www.giosg.com/support/user":
            self.bot.react_to_customer_service_agent(chat_id)
        elif response_value == "https://www.giosg.com/support/manager":
            self.bot.react_to_manager_user(chat_id)
        elif response_value == "https://www.giosg.com/support/developer":
            self.bot.react_to_developer(chat_id)

        return {'detail': 'OK'}
