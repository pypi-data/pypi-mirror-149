import sys
import os
import unittest

sys.path.append(os.path.join(os.getcwd(), '..'))

from client_dist.client.common.variables import *


class TestClass(unittest.TestCase):
    """Класс для Юнит тестов"""
    def test_create_presence_eaual(self):
        test = create_presence()
        test[TIME] = 1645608843.0250275
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_create_presence_notnequal(self):
        test = create_presence()
        test[TIME] = 1645608843.0250275
        self.assertNotEqual(test, {ACTION: PRESENCE, TIME: 1645608843.0250275, USER: {ACCOUNT_NAME: 'User'}})

    def test_process_ans_200_equal(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200: OK')

    def test_process_ans_200_notequal(self):
        self.assertNotEqual(process_ans({RESPONSE: 200}), 'bad_response')

    def test_process_ans_400_equal(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), '400: Bad Request')

    def test_process_ans_400_notequal(self):
        self.assertNotEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}), 'bad_response')

    def test_process_ans_error(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
