import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE, \
    ENCODING, RESPONSE, ERROR
from common.utils import get_message, send_message


class TestSocket:
    def __init__(self, test_message):
        self.test_message = test_message
        self.encoded_message = None

    def recv(self, max_length):
        json_message = json.dumps(self.test_message)
        return json_message.encode(ENCODING)

    def send(self, message):
        json_message = json.dumps(self.test_message)
        self.encoded_message = json_message.encode(ENCODING)


class TestUtilsClass(unittest.TestCase):
    test_message = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'test'
        }
    }
    success_dict = {RESPONSE: 200}
    error_dict = {RESPONSE: 400, ERROR: 'Bad Request'}

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_message_returns_type_dict(self):
        test_socket = TestSocket(self.test_message)
        response = get_message(test_socket)
        self.assertIsInstance(response, dict)

    def test_get_message_response_equals(self):
        test_socket = TestSocket(self.test_message)
        response = get_message(test_socket)
        self.assertDictEqual(response, self.test_message)

    def test_send_message_raises_type_error(self):
        test_socket = TestSocket(self.test_message)
        self.assertRaises(
            TypeError,
            send_message,
            (test_socket, self.test_message)
        )

    def test_send_message_encoding(self):
        test_socket = TestSocket(self.test_message)
        send_message(test_socket, self.test_message)
        sended_message = json.loads(test_socket.encoded_message)
        self.assertDictEqual(sended_message, self.test_message)

    if __name__ == '__main__':
        unittest.main()