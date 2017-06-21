# -*- coding: utf-8 -*-

from flask import request, abort
from flask_restful import Resource
from bot import Jelpperi
from conf import BOT_USER_ID, BOT_USER_API_TOKEN, BOT_USER_ORGANIZATION_ID, SERVICE_URL, ALLOWED_ROOM_ID, SECRET_STRING
import requests
import urlparse
import json


# Usable headers for all the requests to giosg's system
HEADERS = {
    "Authorization": "Token {}".format(BOT_USER_API_TOKEN),
    "content_type": "application/json"
}


class ChatMessageAPIView(Resource):

    def __init__(self):
        if request.args.get('secret') != SECRET_STRING:
            abort(403)

    def post(self):
        response = self.handle_resource()
        if response:
            response.raise_for_status()
        return {'detail': 'Ok'}

    def handle_resource(self):
        jelpperi = Jelpperi()
        json_data = request.get_json(force=True)

        # Format the data
        try:
            resource = json_data['resource']
            chat_id = json_data['resource']['chat_id']
            room_id = json.loads(get_room_id(chat_id).content)['room_id']
            user_client_id = json.loads(get_user_client_id().content)['results'][0]['id']
        except KeyError:
            return

        # Patch user client update
        if resource['type'] == 'msg' or resource['type'] == 'action':
            update_user_client_presence(user_client_id)

        # If the room is not the allowed room, then just return
        if room_id != ALLOWED_ROOM_ID:
            return

        # Visitor side messages
        if resource['sender_type'] == 'visitor':
            if resource['type'] == 'msg':
                # Check all the visitor's message if they contain wrongly typed giosg
                payload = jelpperi.giosg_name_checker(resource['message'])
                if payload:
                    create_chat_memberhip(chat_id)
                    return requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )

                # Otherwise check if the visitor is asking the weather
                if "weather" in resource['message'].lower():
                    payload = jelpperi.get_weather_forecast("Helsinki", "fi")
                    create_chat_memberhip(chat_id)
                    return requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )

            elif resource['type'] == 'action':
                if resource['response_value'] in ['yes', 'no', 'maybe']:
                    payload = jelpperi.handle_feedback()
                    return requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )
                elif resource['response_value'] in ['correct', 'wrong']:
                    payload, correct = jelpperi.handle_giosg_name(resource['response_value'])
                    return requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )
        elif resource['sender_type'] == 'user' and resource['message']:
            # Check for lunch request
            if resource['message'] == '/lunch':
                payload = jelpperi.get_lunch()
                return requests.post(
                    "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                    headers=HEADERS, json=payload, timeout=5
                )

            # Check for feedback request
            elif resource['message'] == '/feedback':
                payload = jelpperi.get_feedback()
                return requests.post(
                    "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                    headers=HEADERS, json=payload, timeout=5
                )

            # Check for coffee request
            elif resource['message'] == '/coffee':
                create_chat_memberhip(chat_id)
                payload = jelpperi.get_covfefe()
                return requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            # Check for feedback request
            elif resource['message'] == '/feedback':
                create_chat_memberhip(chat_id)
                payload = jelpperi.get_feedback()
                return requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            # Check for end chat request
            elif resource['message'] == '/end_chat':
                create_chat_memberhip(chat_id)
                payload = {"is_ended": True}
                return requests.patch("{}/api/v5/users/{}/chats/{}".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            elif resource['message'].startswith('/giphy '):
                create_chat_memberhip(chat_id)
                message = resource['message'][7:]
                payload = jelpperi.get_giphy_link(message, bool(urlparse.urlparse(message).scheme))
                return requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)


def create_chat_memberhip(chat_id):
    """
    Adds the bot as a member to the given chat.
    """
    requests.post(
        "{}/api/v5/orgs/{}/owned_chats/{}/memberships".format(SERVICE_URL, BOT_USER_ORGANIZATION_ID, chat_id),
        headers=HEADERS, json={"member_id": BOT_USER_ID, "is_participating": False, "composing_status": "idle"}, timeout=5
    )


def get_user_client_id():
    return requests.get(
        "{}/api/v5/orgs/{}/users/{}/clients".format(SERVICE_URL, BOT_USER_ORGANIZATION_ID, BOT_USER_ID),
        headers=HEADERS, timeout=5
    )


def update_user_client_presence(client_id):
    return requests.patch(
        "{}/api/v5/orgs/{}/users/{}/clients/{}".format(SERVICE_URL, BOT_USER_ORGANIZATION_ID, BOT_USER_ID, client_id),
        headers=HEADERS, json={"presence_expires_in": 60}, timeout=5
    )


def get_room_id(chat_id):
    return requests.get(
        "{}/api/v5/orgs/{}/owned_chats/{}".format(SERVICE_URL, BOT_USER_ORGANIZATION_ID, chat_id),
        headers=HEADERS, timeout=5
    )
