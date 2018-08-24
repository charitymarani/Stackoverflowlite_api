'''tests/test_register_user.py'''
import unittest
import json
import ast
from application import create_app
from manage import DBMigration


class RegisterUserTestCase(unittest.TestCase):
    '''class representing BookModel Test case'''

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.migrate = DBMigration()
        self.client = self.app.test_client

        with self.app.app_context():
            self.migrate.create_all()

    def test_register_user(self):
        '''test handling user registration'''
        # test successfull user registration
        result = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps(
            {"name": "Njeri ", "username": "alice", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data = ast.literal_eval(result.data)
        self.assertEqual(result.status_code, 201)
        self.assertEqual("User successfully added", my_data["message"])
        # test double registration of the same user
        result2 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps(
            {"name": "Njeri", "username": "alice", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data2 = ast.literal_eval(result2.data)
        self.assertEqual(result2.status_code, 409)
        self.assertEqual("Registration failed. Username already exists",
                         my_data2["message"])
        # test registration using an already existent email
        result3 = self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps(
            {"name": "charity", "username": "charo", "email": "njeri@to.com", "password": "Test123", "confirm_password": "Test123"}))
        my_data3 = ast.literal_eval(result3.data)
        self.assertEqual(result3.status_code, 409)
        self.assertEqual("Registration failed. Email entered already exists",
                         my_data3["message"])

        # test registration using empty fields
        result6 = self.client().post('/api/v1/auth/register',
                                     content_type="application/json", data=json.dumps({}))
        my_data6 = ast.literal_eval(result6.data)
        self.assertEqual(result6.status_code, 400)
        self.assertEqual("Fields cannot be empty", my_data6["message"])
        # test registration using empty data strings
        result7 = self.client().post('/api/v1/auth/register', content_type="application/json",
                                     data=json.dumps({"name": "Fred", "username": None, "email": None, "password": None, "confirm_password": None}))
        my_data7 = ast.literal_eval(result7.data)
        self.assertEqual(result7.status_code, 400)
        self.assertEqual("Some fields are missing",
                         my_data7["message"])

    def tearDown(self):
        with self.app.app_context():
            """removes the db and the context"""
            self.migrate.drop_tables()


if __name__ == "__main__":
    unittest.main()
