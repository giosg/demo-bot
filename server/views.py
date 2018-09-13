# -*- coding: utf-8 -*-

from flask import request, abort
from flask_restful import Resource
from bot import ChatBot
from conf import SECRET_STRING


class APIView(Resource):
    """
    ASDASD
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
        self.authentication = json_data.get('auth_app_user')

        # If resource, resource_id, or authentication
        # data is missing we can't continue
        if not (self.resource or self.authentication or self.resource_id):
            abort(400)

        # Format the data and get needed resources
        # 1. user_id
        # 2. authentication token
        self.user_id = self.authentication.get('user_id')
        self.token = self.authentication.get('access_token')

        # Initialize chat bot
        self.bot = ChatBot()

        # Update bot's user client or create new user client if none found
        self.bot.update_or_create_user_client(self.user_id)


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
        allowed_to_join = self.bot.is_allowed_to_join(user_id=self.user_id, chat_id=self.resource_id)

        # Bot was allowed to join to the chat
        if allowed_to_join:
            self.bot.join_to_chat(user_id=self.user_id, chat_id=self.resource_id)
            self.bot.send_welcoming_message(user_id=self.user_id, chat_id=self.resource_id)
        return {'detail': 'OK'}


class ChatMessageAPIView(APIView):
    """
    API view for handling routed chat message webhooks.
    In this case the bot has receiver a notification
    about new chat message that has been added.
    """
    def post(self):
        super(ChatAPIView, self).post()
        chat_id = self.resource.get('chat_id')

        # Never react to own message
        if self.resource.get('sender_id') == self.user_id:
            return

        # Check is it either:
        # 1. A visitor message
        if self.resource.get('type') != 'action':
            self.bot.handle_visitor_message(user_id=self.user_id, chat_id=chat_id)
        # 2. A response to welcoming message
        elif self.resource.get(''):
            pass
        # 3. A response to feedback
        elif self.resource.get(''):
            self.bot.check_operator_online_status()

        return {'detail': 'OK'}
