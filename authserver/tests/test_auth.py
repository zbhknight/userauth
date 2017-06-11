import unittest
import json
import time

from base import BaseTestCase

class TestAuthBlueprint(BaseTestCase):

    def register_user(self, email, password):
        return self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    email=email,
                    password=password)),
                content_type='application/json')

    def login_user(self, email, password):
        return self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=email,
                    password=password)),
                content_type='application/json')

    def logout_user(self, auth_token):
        return self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer %s' % auth_token))

    def test_registration(self):
        with self.client:
            response = self.register_user('aaa@gmail.com', '123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_reg_with_exist_user(self):
        self.register_user('abc@gmail.com', '123')
        with self.client:
            response = self.register_user('abc@gmail.com', '123')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)

    def test_reg_user_login(self):
        with self.client:
            rsp = self.register_user('knight@gmail.com', '123')
            data = json.loads(rsp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(rsp.status_code, 201)

            rsp = self.login_user('knight@gmail.com', '123')
            data = json.loads(rsp.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['user'])
            self.assertTrue(data['user']['token'])
            self.assertEqual(rsp.status_code, 200)

    def test_non_reg_user_login(self):
        with self.client:
            rsp = self.login_user('knight@gmail.com', '123')
            data = json.loads(rsp.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertEqual(rsp.status_code, 404)

    #def test_user_status(self):
    #    with self.client:
    #        rsp = self.register_user('knight@gmail.com', '123')
    #        rsp = self.client.get(
    #                '/auth/status',
    #                headers=dict(
    #                    Authorization='Bearer %s' % json.loads(rsp.data.decode()).get('auth_token'))
    #                )
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertTrue(data['data']['email'] == 'knight@gmail.com')
    #        self.assertEqual(rsp.status_code, 200)

    #def test_valid_logout(self):
    #    """Logout before expires"""
    #    with self.client:
    #        rsp = self.register_user('knight@gmail.com', '123')
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertTrue(data['auth_token'])
    #        self.assertEqual(rsp.status_code, 201)

    #        rsp = self.login_user('knight@gmail.com', '123')
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertTrue(data['auth_token'])
    #        self.assertEqual(rsp.status_code, 200)

    #        rsp = self.logout_user(data.get('auth_token'))
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertEqual(rsp.status_code, 200)

    #def test_invalid_logout(self):
    #    with self.client:
    #        rsp = self.register_user('knight@gmail.com', '123')
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertTrue(data['auth_token'])
    #        self.assertEqual(rsp.status_code, 201)

    #        rsp = self.login_user('knight@gmail.com', '123')
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'success')
    #        self.assertTrue(data['auth_token'])
    #        self.assertEqual(rsp.status_code, 200)

    #        time.sleep(6)

    #        rsp = self.logout_user(data.get('auth_token'))
    #        data = json.loads(rsp.data.decode())
    #        self.assertTrue(data['status'] == 'fail')
    #        self.assertEqual(rsp.status_code, 401)

if __name__ == '__main__':
    unittest.main()
