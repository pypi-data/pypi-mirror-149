import unittest
import os
import sys

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    ERROR, RESPONSE
from server import process_client_message
from copy import deepcopy


class TestServerClass(unittest.TestCase):
    test_time = 1.1
    success_dict = {RESPONSE: 200}
    error_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    test_message = {
        ACTION: PRESENCE,
        TIME: test_time,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_process_client_message_success(self):
        response = process_client_message(self.test_message)
        self.assertDictEqual(response, self.success_dict)

    def test_process_client_message_wrong_action(self):
        message = deepcopy(self.test_message)
        message[ACTION] = 'wrong_action'
        response = process_client_message(message)
        self.assertDictEqual(response, self.error_dict)

    def test_process_client_message_without_time(self):
        message = deepcopy(self.test_message)
        message[TIME] = None
        response = process_client_message(message)
        self.assertDictEqual(response, self.error_dict)

    def test_process_client_message_without_user(self):
        message = deepcopy(self.test_message)
        message[USER] = None
        response = process_client_message(message)
        self.assertDictEqual(response, self.error_dict)

    def test_process_client_message_wrong_account_name(self):
        message = deepcopy(self.test_message)
        message[USER][ACCOUNT_NAME] = 'not_guest'
        response = process_client_message(message)
        self.assertDictEqual(response, self.error_dict)

    if __name__ == '__main__':
        unittest.main()