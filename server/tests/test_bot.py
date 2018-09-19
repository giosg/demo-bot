from server.bot import ChatBot
import responses
import unittest


class BotTest(unittest.TestCase):

    def setUp(self):
        self.bot = ChatBot({
            'access_token': '<ACCESS_TOKEN>',
            'token_type': 'Bearer',
            'user_id': 'user1',
            'organization_id': 'org1',
        })

    @responses.activate
    def test_joins_new_routed_chat(self):
        pass
