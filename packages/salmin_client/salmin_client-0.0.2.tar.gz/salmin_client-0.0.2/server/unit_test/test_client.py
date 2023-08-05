from unittest import TestCase, main
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, PRESENCE, RESPONSE, ERROR, TIME, USER, ACCOUNT_NAME
from client import create_presence, process_ans


class TestClient(TestCase):
    def test_def_presence(self):
        test = create_presence()
        test[TIME] = 1.2
        self.assertEqual(test, {
        ACTION: PRESENCE,
        TIME: 1.2,
        USER: {
            ACCOUNT_NAME: 'Oleg'
        }
    })

    def test_200_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 OK')

    def test_400_ans(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400 Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    main()
