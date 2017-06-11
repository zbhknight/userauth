import unittest

from base import BaseTestCase
from authService import AuthService

class TestAuthService(BaseTestCase):

    def test_create_user(self):
        service = AuthService()
        service.create_user('a@a.com', '123')
        self.assertTrue('a@a.com' in service._users)
        self.assertEqual(service._users['a@a.com']['password'], '123')
        self.assertTrue(service._users['a@a.com']['id'] > 0)

    def test_check_user_password(self):
        service = AuthService()
        _user = service.check_user_password('aa', 'bb')
        self.assertFalse(_user['id'])
        service.create_user('a@a.com', '123')
        _user = service.check_user_password('a@a.com', '123')
        self.assertTrue(_user['id'])
        self.assertFalse(service.check_user('abc'))
        self.assertTrue(service.check_user('a@a.com'))

if __name__ == "__main__":
    unittest.main()
