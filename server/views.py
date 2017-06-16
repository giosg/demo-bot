# -*- coding: utf-8 -*-

from flask import request
from flask_restful import Resource
from bot import Jelpperi
from conf import BOT_USER_ID, BOT_USER_API_TOKEN, BOT_USER_ORGANIZATION_ID, SERVICE_URL
import requests
import urlparse


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
            resource_id = json_data['resource_id']  # noqa
            action = json_data['action']  # noqa
            chat_id = json_data['resource']['chat_id']
            print chat_id
        except KeyError:
            return

        # Visitor side messages
        if resource['sender_type'] == 'visitor':
            if resource['type'] == 'msg':
                # Check all the visitor's message if they contain wrongly typed giosg
                payload = jelpperi.giosg_name_checker(resource['message'])
                if payload:
                    requests.post(
                        "http://localhost:8000/api/v5/orgs/{}/owned_chats/{}/memberships".format(BOT_USER_ORGANIZATION_ID, chat_id),
                        headers=HEADERS, json={"member_id": BOT_USER_ID, "is_participating": True, "composing_status": "idle"}, timeout=5
                    )
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
        elif resource['sender_type'] == 'user':
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
                payload = jelpperi.get_covfefe()
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            # Check for feedback request
            elif resource['message'] == '/feedback':
                payload = jelpperi.get_feedback()
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

            elif resource['message'].startswith('/giphy '):
                message = resource['message'][7:]
                payload = jelpperi.get_giphy_link(message, bool(urlparse.urlparse(message).scheme))
                requests.post("{}/api/v5/users/{}/chats/{}/messages".format(SERVICE_URL, BOT_USER_ID, chat_id), headers=HEADERS, json=payload, timeout=5)

        return {'detail': 'Ok'}
