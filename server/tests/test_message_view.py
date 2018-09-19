from server.conf import SECRET_STRING
from server import server
from mock import patch
import unittest


class MessageAPIViewTest(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.client = server.app.test_client()

        self.resource = {
            "id": "8a94b3f1-d8a9-4530-b1f1-b757a8a57078",
            "type": "autosuggest",
            "chat_id": "450fc49e-277e-4dd6-af0f-6e9dcb885b09",
            "created_at": "2015-02-13T11:30:03.045",
            "sender_type": "user",
            "sender_id": "7c94ae79-a4b4-4eea-ac23-24c16f910080",
            "sender_public_name": "Customer Service",
            "sender_name": "John Smith",
            "message": "How may I help you?",
            "is_encrypted": False,
            "sensitive_data_purged_at": None,
            "selected_reply_suggestion_id": None,
            "selected_reply_suggestion": None,
            "attachments": [],
            "response_to_message_id": None,
            "response_to_attachment_id": None,
            "response_to_attachment": None,
            "response_to_action_id": None,
            "response_to_action": None,
            "response_value": None
        }
        self.valid_data = {
            "channel": "/api/v5/users/dabfd452-cbc0-4eff-aaac-f4e125db0fe4/routed_chats/450fc49e-277e-4dd6-af0f-6e9dcb885b09/messages",
            "action": "added",
            "resource_id": "e1549f4d-d2a6-4efb-b64c-e977b0a5ba96",
            "app_user_auth": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmb28iOiJiYXIifQ.JsxySWmKqmsd7BTXRi3JnmkFS4kJJTU_NYUN2NcfsP8",
                "token_type": "Bearer",
                "expires_in": 300,
                "user_id": "dabfd452-cbc0-4eff-aaac-f4e125db0fe4",
                "organization_id": "7f9e9580-095b-42c7-838c-c04e667b26f7"
            },
            "resource": self.resource
        }

        # Mock handle_new_user_chat_message method
        self.handle_new_user_chat_message_patcher = patch('server.bot.ChatBot.handle_new_user_chat_message', auto_spec=True)
        self.mock_handle_new_user_chat_message = self.handle_new_user_chat_message_patcher.start()
        self.addCleanup(self.handle_new_user_chat_message_patcher.stop)

    def test_handle_post_request(self):
        response = self.client.post('/messages?secret=' + SECRET_STRING, json=self.valid_data)
        self.assertEqual(response._status_code, 200)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 1)
        self.mock_handle_new_user_chat_message.assert_any_call(self.resource)

    def test_return_405_for_get_requests(self):
        response = self.client.get('/messages')
        self.assertEqual(response._status_code, 405)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_405_for_put_requests(self):
        response = self.client.put('/messages')
        self.assertEqual(response._status_code, 405)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_405_for_patch_requests(self):
        response = self.client.patch('/messages')
        self.assertEqual(response._status_code, 405)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_403_if_secret_string_does_not_match(self):
        response = self.client.post('/messages?secret=TestSecret', json=self.valid_data)
        self.assertEqual(response._status_code, 403)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_400_if_data_is_missing_from_request(self):
        response = self.client.post('/messages?secret=' + SECRET_STRING, json={})
        self.assertEqual(response._status_code, 400)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_400_if_resource_is_missing_from_request(self):
        self.valid_data.pop('resource')
        response = self.client.post('/messages?secret=' + SECRET_STRING, json=self.valid_data)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_400_if_authentication_is_missing_from_request(self):
        self.valid_data.pop('app_user_auth')
        response = self.client.post('/messages?secret=' + SECRET_STRING, json=self.valid_data)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)

    def test_return_400_if_resource_id_is_missing_from_request(self):
        self.valid_data.pop('resource_id')
        response = self.client.post('/messages?secret=' + SECRET_STRING, json=self.valid_data)
        self.assertEqual(response._status_code, 400)
        self.assertEqual(self.mock_handle_new_user_chat_message.call_count, 0)
