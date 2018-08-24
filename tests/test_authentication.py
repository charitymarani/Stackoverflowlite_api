import unittest
import json
import ast
from flask_jwt_extended import get_jwt_identity, create_access_token
from ..application import create_app
from manage import Migration


class TestBase(unittest.TestCase):
    '''class to tests app.py'''

    def setUp(self):
        '''create a test client'''
        self.app = create_app(config_name="testing")
        self.migrate = Migration()
        self.client = self.app.test_client
        self.client().post('/api/v1/auth/register', content_type='application/json', data=json.dumps(
            {"name": "chari", "username": "charity", "email": "charity@gmail.com", "password": "Test123", "confirm_password": "Test123"}))
        with self.app.app_context():
            self.migrate.create_all()

    def tearDown(self):
        """removes the db and the context"""
        self.migrate.drop_tables()


class TestAuth(TestBase):
    '''class to test authentication action'''

    def test_user_login(self):
            # login successful
        result = self.client().post('/api/v1/auth/login', content_type="application/json",
                                    data=json.dumps({"username": "charity", "password": "Test123"}))
        self.assertEqual(result.status_code, 200)
        my_data1 = ast.literal_eval(result.data.decode())
        self.assertIn("token", result.data)
        # no data passed
        result2 = self.client().post('/api/v1/auth/login',
                                     content_type="application/json", data=json.dumps({}))
        self.assertEqual(result2.status_code, 400)
        my_data2 = ast.literal_eval(result2.data.decode())
        self.assertEqual("Fields cannot be empty", my_data2["message"])
        # empty strings
        result3 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                     data=json.dumps({"username": "", "password": ""}))
        self.assertEqual(result3.status_code, 400)
        my_data3 = ast.literal_eval(result3.data.decode())
        self.assertEqual("Username or password missing", my_data3["message"])
        # incorrect username
        result4 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                     data=json.dumps({"username": "sharon", "password": "Test123"}))
        self.assertEqual(result4.status_code, 401)
        my_data4 = ast.literal_eval(result4.data.decode())
        self.assertEqual("Incorrect username", my_data4["message"])
        # incorrect password
        result5 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                     data=json.dumps({"username": "charity", "password": "test123"}))
        self.assertEqual(result5.status_code, 401)
        my_data5 = ast.literal_eval(result5.data.decode())
        self.assertEqual("Incorrect password", my_data5["message"])

    def test_logout(self):
        # test logout
         # login
        result = self.client().post('/api/v1/auth/login', content_type="application/json",
                                    data=json.dumps({"username": "charity", "password": "Test123"}))
        self.assertEqual(result.status_code, 200)
        my_data = ast.literal_eval(result.data.decode())
        token = my_data["token"]
        # logout
        result2 = self.client().post('/api/v1/auth/logout',
                                     headers=dict(Authorization="Bearer " + token))
        self.assertEqual(result2.status_code, 200)
        my_result = result2.data
        self.assertIn("Successfully logged out", str(my_result))

    def test_reset_password(self):
        '''test reset password method = ("POST")'''
        # successful
        result4 = self.client().post('/api/v1/auth/reset_password',
                                     content_type="application/json",
                                     data=json.dumps({"username": "charity"}))
        self.assertEqual(result4.status_code, 200)


if __name__ == "__main__":
    unittest.main()
