# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from bot import Jelpperi
from conf import BOT_USER_ID, BOT_USER_API_TOKEN, BOT_USER_ORGANIZATION_ID, SERVICE_URL, ALLOWED_ROOM_ID
import requests
import urlparse
import json


# Usable headers for all the requests to giosg's system
HEADERS = {
    "Authorization": "Token {}".format(BOT_USER_API_TOKEN),
    "content_type": "application/json"
}


class ChatMessageAPIView(Resource):
    def post(self):
        jelpperi = Jelpperi()
        json_data = request.get_json(force=True)

        # Format the data
        try:
            resource = json_data['resource']
            chat_id = json_data['resource']['chat_id']
            room_id = json.loads(get_room_id(chat_id).content)['room_id']
        except KeyError:
            return

        # If the room is not the allowed room, then just return
        if room_id != ALLOWED_ROOM_ID:
            return

        # Visitor side messages
        if resource['sender_type'] == 'visitor':
            if resource['type'] == 'msg':
                # Check all the visitor's message if they contain wrongly typed giosg
                payload = jelpperi.giosg_name_checker(resource['message'])
                if payload:
                    participate_chat(chat_id)
                    requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )

            elif resource['type'] == 'action':
                if resource['response_value'] in ['yes', 'no', 'maybe']:
                    payload = jelpperi.handle_feedback()
                    requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )
                elif resource['response_value'] in ['correct', 'wrong']:
                    payload = jelpperi.handle_giosg_name(resource['response_value'])
                    requests.post(
                        "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                        headers=HEADERS, json=payload, timeout=5
                    )
        elif resource['sender_type'] == 'user' and resource['message']:
            # Check for lunch request
            if resource['message'] == '/lunch':
                payload = jelpperi.get_lunch()
                requests.post(
                    "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                    headers=HEADERS, json=payload, timeout=5
                )

            # Check for feedback request
            elif resource['message'] == '/feedback':
                payload = jelpperi.get_feedback()
                requests.post(
                    "{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id),
                    headers=HEADERS, json=payload, timeout=5
                )

            # Check for coffee request
            elif resource['message'] == '/coffee':
                participate_chat(chat_id)
                payload = jelpperi.get_covfefe()
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            # Check for feedback request
            elif resource['message'] == '/feedback':
                participate_chat(chat_id)
                payload = jelpperi.get_feedback()
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            # Check for end chat request
            elif resource['message'] == '/end_chat':
                participate_chat(chat_id)
                payload = {"is_ended": True}
                response = requests.patch("{}/api/v5/users/{}/chats/{}".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)
                print response

            elif resource['message'].startswith('/giphy '):
                participate_chat(chat_id)
                message = resource['message'][7:]
                payload = jelpperi.get_giphy_link(message, bool(urlparse.urlparse(message).scheme))
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

        return {'detail': 'Ok'}


def participate_chat(chat_id):
    requests.post(
        "http://localhost:8000/api/v5/orgs/{}/owned_chats/{}/memberships".format(BOT_USER_ORGANIZATION_ID, chat_id),
        headers=HEADERS, json={"member_id": BOT_USER_ID, "is_participating": True, "composing_status": "idle"}, timeout=5
    )


def leave_chat(chat_id):
    requests.post(
        "http://localhost:8000/api/v5/orgs/{}/owned_chats/{}/memberships".format(BOT_USER_ORGANIZATION_ID, chat_id),
        headers=HEADERS, json={"member_id": BOT_USER_ID, "is_participating": False, "composing_status": "idle"}, timeout=5
    )


def get_room_id(chat_id):
    return requests.get(
        "http://localhost:8000/api/v5/orgs/{}/owned_chats/{}".format(BOT_USER_ORGANIZATION_ID, chat_id),
        headers=HEADERS, timeout=5
    )
