from server.conf import SECRET_STRING
from server import server
import mock
import pytest


TEST_DATA = {
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
    "resource": {
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
}


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    yield client


@pytest.fixture(scope='session', autouse=True)
def handle_new_user_chat_message_mocked():
    with mock.patch('server.bot.ChatBot.handle_new_user_chat_message') as _fixture:
        yield _fixture


def test_handle_post_request(client, handle_new_user_chat_message_mocked):
    rv = client.post('/messages?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 200
    assert handle_new_user_chat_message_mocked.call_count == 1


def test_return_405_for_get_requests(client):
    rv = client.get('/messages')
    assert rv._status_code == 405


def test_return_405_for_put_requests(client):
    rv = client.put('/messages')
    assert rv._status_code == 405


def test_return_405_for_patch_requests(client):
    rv = client.patch('/messages')
    assert rv._status_code == 405


def test_return_403_if_secret_string_does_not_match(client):
    rv = client.post('/messages?secret=TestSecret', json=TEST_DATA)
    assert rv._status_code == 403


def test_return_400_if_data_is_missing_from_request(client):
    rv = client.post('/messages?secret=' + SECRET_STRING, json={})
    assert rv._status_code == 400


def test_return_400_if_resource_is_missing_from_request(client):
    TEST_DATA.pop('resource')
    rv = client.post('/messages?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400


def test_return_400_if_authentication_is_missing_from_request(client):
    TEST_DATA.pop('app_user_auth')
    rv = client.post('/messages?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400


def test_return_400_if_resource_id_is_missing_from_request(client):
    TEST_DATA.pop('resource_id')
    rv = client.post('/messages?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400
