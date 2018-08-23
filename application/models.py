'''models.py containing models for the API'''
import random
import string
from uuid import uuid4

ALL_QUESTIONS = {}


class Questions():
    '''class to represent question and answer model'''

    def __init__(self):
        self.question = {}
        self.answer = {}

    def get_all(self):
        '''return all questions from ALL_QUESTIONS dictionary'''
        return ALL_QUESTIONS

    def get_single_question(self, question_id):
        '''get single question from ALL_QUESTIONS using id'''
        if question_id in ALL_QUESTIONS:
            return ALL_QUESTIONS[question_id]

        return {"message": "Question not found"}

    def post_question(self, topic, title, details, question_id):
        '''add a question to ALL_QUESTIONS'''

        if title in ALL_QUESTIONS:
            return {"message": "Question  entered already exists"}

        self.question["title"] = title
        self.question["details"] = details
        self.question["topic"] = topic
        self.question["question_id"] = question_id

        ALL_QUESTIONS[question_id] = self.question

        return {"message": "Question added successfully"}

    # delete question

    def delete(self, question_id):
        '''delete a question by its id'''
        if question_id in ALL_QUESTIONS:
            del ALL_QUESTIONS[question_id]
            return {"message": "Question {} deleted successfully"
                    .format(question_id)}

        return {"message": "Question you are trying to delete doesn't exist"}


class Answers():
    '''answer class conaining answer related operations'''

    def __init__(self, answer_body):
        '''constructor method to initialize an object'''
        self.answer_body = answer_body

    def serialize_answer(self, count, question_id):
        '''take answer object and return __dict__ representation'''
        return dict(
            answer=self.answer_body,
            ans_id=count,
            accepted=False,
            question_id=question_id
        )
