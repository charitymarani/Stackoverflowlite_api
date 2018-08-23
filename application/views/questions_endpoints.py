import re
from flask import Flask, request, jsonify, make_response
from uuid import uuid4
from flask_restful import Resource
from ..models import Questions, Answers, ALL_QUESTIONS
from ..views.checker import question_already_exist, answer_already_exist
from .. import models,app

all_answers = list()

MY_QUESTION = models.Questions()

'''question related routes'''


class PostQuestion(Resource):
    def post(self):

        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})

        title = data.get('title')
        topic = data.get('topic')
        details = data.get('details')
        question_id = data.get('question_id')

        if title is None or not title:
            return ({"message": "Enter title"})
        if details is None or not details:
            return jsonify({"message": "Enter details for your question"})

        response = jsonify(MY_QUESTION.post_question(topic,
                                                     title, details, question_id))
        response.status_code = 201
        return response


class GetAllQuestions(Resource):
    def get(self):
        ''' get all questions method="GET"'''
        get_questions = MY_QUESTION.get_all()
        response = jsonify(get_questions)
        response.status_code = 200

        return response


class GetSingleQuestion(Resource):
    def get(self, question_id):
        '''endpoint to get question by id'''
        get_question = MY_QUESTION.get_single_question(question_id)
        response = jsonify(get_question)
        response.status_code = 200

        return response


class DeleteQuestion(Resource):
    def delete(self, question_id):
        '''delete a question when logged in, method=DELETE'''
        response = jsonify(MY_QUESTION.delete(question_id))
        response.status_code = 200

        return response


class PostAnswer(Resource):

    def post(self, question_id):
        ''' endpoint for answering a question'''
        answer_body = request.json.get('answer')
        if not answer_body:
            return jsonify({'message': 'Provide an answer'})

        if not question_already_exist(question_id):
            return jsonify({'message': 'The question' +
                            ' does not exist'})
        if answer_already_exist(all_answers, 'answer', answer_body):
            return jsonify(
                {'message': 'This answer is already given'})
        count = 1
        for item in all_answers:
            count += 1

        answer = Answers(answer_body)
        answer_dict = answer.serialize_answer(
            count, question_id)
        all_answers.append(answer_dict)
        response = jsonify({'message': 'Answer posted successfully'})
        response.status_code = 201
        return response
