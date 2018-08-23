import unittest
import json
import ast
from application import create_app


class TestBase(unittest.TestCase):
    '''class to tests app.py'''

    def setUp(self):
        '''create a test client'''
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

        self.question = {"topic": "java",
                         "title": "What is java", "details": "i want to know java",
                         "question_id": 1
                         }
        self.answer = {
            "answer": "This is the answer"
        }

    def tearDown(self):
        '''clear list data for every test case to be atomic'''
        self.app_context.pop()

    def test_post_question(self):
        # post_question
        response = self.client().post(
            '/api/v1/questions',
            data=json.dumps(dict(
                question_id=2,
                topic='python',
                details='I do not seem to understand jwt,what is it where  is it use',
                title='What is token based authentication?'
            )),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)

    def test_post_answer(self):
        self.client().post(
            'api/v1/questions',
            data=json.dumps(self.question),
            content_type='application/json'
        )
        # post answer
        resp = self.client().post('/api/v1/questions/1/answers',
                                  data=json.dumps(self.answer),
                                  content_type='application/json')

        self.assertEqual(resp.status_code, 201)

    def test_get_all_questions(self):
        # get all questions
        response = self.client().post('/api/v1/questions',
                                      data=json.dumps(dict(
                                          question_id=3,
                                          topic='python',
                                          details='I do not seem to understand jwt,what is it where  is it use',
                                          title='What is token based authentication?'
                                      )),
                                      content_type='application/json'
                                      )

        self.assertEqual(response.status_code, 201)
        new_quest = self.client().post('/api/v1/questions',

                                       data=json.dumps(self.question),
                                       content_type='application/json')
        self.assertEqual(new_quest.status_code, 201)
        response = self.client().get('/api/v1/questions')
        self.assertEqual(response.status_code, 200)

    def test_get_question_by_id(self):
        """Test that the API retrieve a question by id"""
        # post a new question to get a question id in the response
        response = self.client().post('/api/v1/questions',
                                      data=json.dumps(dict(
                                          question_id=3,
                                          topic='python',
                                          details='I do not seem to understand jwt,what is it where  is it use',
                                          title='What is token based authentication?'
                                      )),
                                      content_type='application/json'
                                      )

        self.assertEqual(response.status_code, 201)
        response = self.client().get(
            '/api/v1/questions/3')
        # check that the server responds with the correct status code
        self.assertEqual(response.status_code, 200)

        # test that the response contains the correct question
        self.assertIn("What is token based authentication?",
                      str(response.data))

    def test_delete_question(self):
        new_question = self.client().post('/api/v1/questions',
                                          data=json.dumps(self.question),
                                          content_type='application/json')
        self.assertEqual(new_question.status_code, 201)
        res = self.client().delete('/api/v1/questions/1')

        self.assertEqual(res.status_code, 200)
        # test to check whether deleted item exists
        result = self.client().get('/api/v1/questions/1')
        self.assertIn("Question not found", str(result.data))
