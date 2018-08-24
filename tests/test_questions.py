import unittest
import json
import ast
from flask_jwt_extended import get_jwt_identity, create_access_token
from application import create_app


class TestBase(unittest.TestCase):
    '''class to tests app.py'''

    def setUp(self):
        '''create a test client'''
        self.app = create_app(config_name="testing")
        self.migrate = DBMigration()
        self.client = self.app.test_client
        self.question = { "topic": "java",
                          "title": "What is java", "details": "i want to know",
                          "answers": [{"1": "Java is an oop language"}]
                          }
        # register and login 2  users
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps(
            {"name": "Jay Jay", "username": "jay", "email": "j@gmail.com", "password": "Test123", "confirm_password": "Test123"}))
        result1 = self.client().post(
            '/api/v1/auth/login', content_type="application/json", data=json.dumps({"username": "jay", "password": "Test123"}))
        user_login = ast.literal_eval(result1.data.decode())
       
        self.user_token = json.loads(user_login.data)['token']
        self.client().post('/api/v1/auth/register', content_type="application/json", data=json.dumps(
            {"name": "Sasha", "username": "sasha", "email": "sasha@gmail.com", "password": "Test123", "confirm_password": "Test123"}))
        result2 = self.client().post('/api/v1/auth/login', content_type="application/json",
                                     data=json.dumps({"username": "sasha", "password": "Test123"}))
        user2_login = ast.literal_eval(result2.data.decode())
        self.user2_token = json.loads(user_login2.data)['token']
        with self.app.app_context():
            self.migrate.create_all()
       
    def tearDown(self):
        '''clear list data for every test case to be atomic'''
        with self.app.app_context():
            self.migrate.drop_tables()

    def test_post_question(self):
        # post_question
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + self.user_token
            ),
            data=json.dumps(dict(
                topic='python',
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)

    def test_post_answer(self):

        # post answer
        resp = self.client().post('/api/v1/questions/1/answers',
                                  headers=dict(
                                      Authorization='Bearer ' + self.user2_token),
                                  data=json.dumps(dict(
                                     
                                      answer='the answer is this and that'
                                  )),
                                  content_type='application/json'
                                  )
        response_data = ast.literal_eval(resp.data.decode())
        self.assertIn("Answer posted successfully", str(resp.data))
        self.assertEqual(resp.status_code, 200)

    def test_accept_answer(self):
        resp = self.client().post('/api/v1/questions/1/answers',
                                  headers=dict(
                                      Authorization='Bearer ' + self.user2_token),
                                  data=json.dumps(dict(
                                      answer='the answer is this and that',
                                      )),
                                  content_type='application/json')
        response_data = ast.literal_eval(resp.data.decode())

        self.assertTrue(response_data['message'] ==
                        'Answer posted successfully')
        self.assertEqual(resp.status_code, 201)
        ac_resp = self.client().patch('/api/v1/questions/1/answers/1/accept',
                                      headers=dict(
                                          Authorization='Bearer ' + self.user_token
                                      ),
                                      data=json.dumps(dict(
                                          accepted=True)),
                                      content_type='application/json')
        respo_data = ast.literal_eval(ac_resp.data.decode())
        self.assertTrue(response_data['message'] == 'Answer accepted')
        self.assertEqual(ac_resp.status_code, 200)

    def test_get_all_questions(self):
        # get all questions
        response = self.client().post(
            '/api/v1/questions',
            headers=dict(
                Authorization='Bearer ' + self.user_token
            ),
            data=json.dumps(dict(
                topic='python',
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )
        response_data = ast.literal_eval(response.data.decode())
        self.assertTrue(response_data['message'] ==
                        'Question added successfully')
        self.assertEqual(response.status_code, 200)
        """Test that a user can get all the questions(GET request)"""
        new_quest = self.client().post('/api/v1/questions',

                                       data=json.dumps(self.question),
                                       content_type='application/json')
        self.assertEqual(new_quest.status_code, 200)
        response = self.client().get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)

    def test_get_question_by_id(self):

        # get question by id

        response = self.client().get(
            '/api/v1/questions/1')
        # check that the server responds with the correct status code
        self.assertEqual(response.status_code, 200)
        # test that the response contains the correct question
        self.assertIn("What is java",
                      str(response.data))
        # delete question

    def test_delete_question(self):

        res = self.client().delete('/api/v1/questions/1',
                                   headers=dict(
                                       Authorization='Bearer ' + self.user2_token))

        self.assertEqual(res.status_code, 200)
        # test to check whether deleted item exists
        result = self.client().get('/api/v1/questions/1')
        self.assertIn("Question not found", str(result.data))
    def test_user_retrieves_all_answers(self):
        """Test user can retrieve all answers to a question"""
        with self.client:
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + self.user_token
                     
                    
                ),
                data=json.dumps(dict(
                    title='psycopg2',
                    topic='databases',
                    details='How is psycopg2 used?'
                )),
                content_type='application/json'
            )
            resp = self.client.post(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + self.user_token
                ),
                data=json.dumps(dict(
                    answer='foloow this link to learn'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/1/answers',
                headers=dict(
                    Authorization='Bearer ' + self.user_token
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)
            
      def test_user_retrieves_all_their_questions(self):
        """Test user can retrieve all their questions"""
        with self.client:
            resp = self.client.post(
                '/api/v2/questions',
                headers=dict(
                    Authorization='Bearer ' + self.user2_token
                ),
                data=json.dumps(dict(
                    title='what wa sthat',
                    topic='python'
                    details='how is git used?'
                )),
                content_type='application/json'
            )
            resp = self.client.get(
                '/api/v2/questions/myquestions',
                headers=dict(
                    Authorization='Bearer ' + self.user2_token
                )
            )
            response_data = json.loads(resp.data.decode())
            self.assertEqual(resp.status_code, 200)


   
