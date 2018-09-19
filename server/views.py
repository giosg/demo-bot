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
        if not (self.resource and self.authentication and self.resource_id):
            abort(400)

        # Format the data and get needed resources
        # 1. user_id
        # 2. authentication token
        self.user_id = self.authentication.get('user_id')
        self.organization_id = self.authentication.get('organization_id')
        self.token = self.authentication.get('access_token')

        # Initialize chat bot
        self.bot = ChatBot(self.authentication)


class ChatAPIView(APIView):
    """
    API view for handling routed chat webhooks.
    In this case the bot has received a notification
    about new chat that has been added.
    """
    def post(self):
        super(ChatAPIView, self).post()
        self.bot.handle_new_routed_chat(self.resource)
        return {'detail': 'OK'}


class ChatMessageAPIView(APIView):
    """
    API view for handling routed chat message webhooks.
    In this case the bot has receiver a notification
    about new chat message that has been added.
    """
    def post(self):
        super(ChatMessageAPIView, self).post()
        self.bot.handle_new_user_chat_message(self.resource)
        return {'detail': 'OK'}
