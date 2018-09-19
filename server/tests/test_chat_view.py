from server.conf import SECRET_STRING
from server import server
import mock
import pytest


TEST_DATA = {
    "channel": "/api/v5/users/dabfd452-cbc0-4eff-aaac-f4e125db0fe4/routed_chats",
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
        "id": "e1549f4d-d2a6-4efb-b64c-e977b0a5ba96",
        "token": "uibdbtmk5etolmjaduaafnqpl2ujzkyr4slkq3cabdai37qm",
        "created_at": "2015-02-13T11:31:36.042",
        "ended_at": None,
        "waiting_started_at": None,
        "updated_at": "2015-02-13T12:38:36.431",
        "room_id": "9926bdfa-56e0-11e5-b98c-6c4008c08dfe",
        "room_name": "Customer Support",
        "room_organization_id": "7f9e9580-095b-42c7-838c-c04e667b26f7",
        "is_private": False,
        "is_real_conversation": False,
        "is_autosuggested": False,
        "is_encrypted": True,
        "encrypted_symmetric_key": "0d59ab43b5704f08b2aec117658f4bc29a9b0c248547404298bb8a3f06eab7206455a0ddfa1d4972a364d7766eccb4ca",
        "message_count": 0,
        "user_message_count": 0,
        "visitor_message_count": 0,
        "has_messages": False,
        "has_user_messages": False,
        "has_visitor_messages": False,
        "first_visitor_message_url": "http://www.customerpage.com/settings",
        "first_visitor_message_url_title": "Profile Settings",
        "autosuggest_url": "http://www.customerpage.com/",
        "autosuggest_url_title": "Site Frontpage",
        "tag_count": 2,
        "is_waiting": True,
        "member_count": 2,
        "user_member_count": 1,
        "visitor_member_count": 1,
        "present_participant_count": 1,
        "present_user_participant_count": 1,
        "present_visitor_participant_count": 1,
        "legacy_conversation_state": "waiting",
        "legacy_room_id": "7sbjsyokgkdmyoifwyaafzll6sdthgar42sbv5c4rhds3yym"
    }
}


@pytest.fixture
def client():
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    yield client


@pytest.fixture(scope='session', autouse=True)
def handle_new_routed_chat_mocked():
    with mock.patch('server.bot.ChatBot.handle_new_routed_chat') as _fixture:
        yield _fixture


def test_handle_post_request(client, handle_new_routed_chat_mocked):
    rv = client.post('/chats?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 200
    assert handle_new_routed_chat_mocked.call_count == 1


def test_return_405_for_get_requests(client):
    rv = client.get('/chats')
    assert rv._status_code == 405


def test_return_405_for_put_requests(client):
    rv = client.put('/chats')
    assert rv._status_code == 405


def test_return_405_for_patch_requests(client):
    rv = client.patch('/chats')
    assert rv._status_code == 405


def test_return_403_if_secret_string_does_not_match(client):
    rv = client.post('/chats?secret=TestSecret', json=TEST_DATA)
    assert rv._status_code == 403


def test_return_400_if_data_is_missing_from_request(client):
    rv = client.post('/chats?secret=' + SECRET_STRING, json={})
    assert rv._status_code == 400


def test_return_400_if_resource_is_missing_from_request(client):
    TEST_DATA.pop('resource')
    rv = client.post('/chats?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400


def test_return_400_if_authentication_is_missing_from_request(client):
    TEST_DATA.pop('app_user_auth')
    rv = client.post('/chats?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400


def test_return_400_if_resource_id_is_missing_from_request(client):
    TEST_DATA.pop('resource_id')
    rv = client.post('/chats?secret=' + SECRET_STRING, json=TEST_DATA)
    assert rv._status_code == 400
