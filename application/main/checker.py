'''checker.py'''
from flask import make_response, jsonify
all_questions = {}
all_answers = {}


def question_already_exist(id):
    ''' check if an object exist'''

    if id in all_questions:
        return make_response(jsonify({'message': 'Question already exists'})), 409
    return False


def answer_already_exist(list_, object_key, object_attr):
    ''' find out if an object exist'''
    if id in all_answers:
        return make_response(jsonify({'message': 'Answer already exists'})), 409
    return False
