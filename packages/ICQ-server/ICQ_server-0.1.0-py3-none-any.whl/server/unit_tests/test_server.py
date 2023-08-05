import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '../../../messenger'))

from server_dist.server.server import process_client_message
from server_dist.server.common.variables import *


class TestClass(unittest.TestCase):
    """Класс для Юнит тестов"""
    def test_process_client_message_response_200_equal(self):
        message = {ACTION: PRESENCE, TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(message), {RESPONSE: 200})

    def test_process_client_message_response_200_notequal(self):
        message = {ACTION: PRESENCE, TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertNotEqual(process_client_message(message), {RESPONSE: 400})

    def test_process_client_message_response_400_no_action_equal(self):
        message = {TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Bad request'})

    def test_process_client_message_response_400_no_action_notequal(self):
        message = {TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertNotEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Good request'})

    def test_process_client_message_response_400_no_time_equal(self):
        message = {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Bad request'})

    def test_process_client_message_response_400_no_time_notequal(self):
        message = {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}
        self.assertNotEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Good request'})

    def test_process_client_message_response_400_no_user_equal(self):
        message = {ACTION: PRESENCE, TIME: 1645608843.0250275}
        self.assertEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Bad request'})

    def test_process_client_message_response_400_no_user_notequal(self):
        message = {ACTION: PRESENCE, TIME: 1645608843.0250275}
        self.assertNotEqual(process_client_message(message), {RESPONSE: 400, ERROR: 'Good request'})
