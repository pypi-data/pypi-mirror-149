import sys
import os
import unittest
import json

sys.path.append(os.path.join(os.getcwd(), '../../../messenger'))

from server_dist.server.common.variables import *
from server_dist.server.common.utils import get_message, send_message


class TestSocket:
    """Тестовый сокет для юнит тестов"""
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.received_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class TestClass(unittest.TestCase):
    """Класс для Юнит тестов"""
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    test_socket = TestSocket(test_dict_send)
    send_message(test_socket, test_dict_send)
    test_sock_ok = TestSocket(test_dict_recv_ok)
    test_sock_err = TestSocket(test_dict_recv_err)

    def test_send_message_equal(self):
        self.assertEqual(self.test_socket.encoded_message, self.test_socket.received_message)

    def test_send_message_notequal(self):
        self.assertNotEqual(self.test_socket.encoded_message, 'bad message')

    def test_send_message_equal_raises(self):
        self.assertRaises(ValueError, send_message, self.test_socket, 1111)

    def test_get_message_200_equal(self):
        self.assertEqual(get_message(self.test_sock_ok), self.test_dict_recv_ok)

    def test_get_message_200_notequal(self):
        self.assertNotEqual(get_message(self.test_sock_ok), self.test_dict_recv_err)

    def test_get_message_400_equal(self):
        self.assertEqual(get_message(self.test_sock_err), self.test_dict_recv_err)

    def test_get_message_400_notequal(self):
        self.assertNotEqual(get_message(self.test_sock_err), self.test_dict_recv_ok)
