import sys
import os
from unittest import TestCase, main
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, RESPONSE, ERROR, TIME, USER, ACCOUNT_NAME
from server import process_client_message


class TestServer(TestCase):
    error_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        self.assertEqual(process_client_message(
                {TIME: '1.1', USER: {ACCOUNT_NAME: 'Oleg'}}), self.error_dict
        )

    def test_incorrect_action(self):
        self.assertEqual(process_client_message(
            {ACTION: 'Error', TIME: 1.1, USER: {ACCOUNT_NAME: 'Oleg'}}), self.error_dict
        )

    def test_no_time(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Oleg'}}), self.error_dict
        )

    def test_no_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1}), self.error_dict
        )

    def test_incorrect_user(self):
        self.assertEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'User'}}), self.error_dict
        )

    def test_ok_check(self):
        self.assertNotEqual(process_client_message(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Oleg'}}), self.error_dict
        )


if __name__ == '__main__':
    main()
