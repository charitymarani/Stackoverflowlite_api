import re
from flask import Flask, request, jsonify, make_response
from uuid import uuid4
from flask_restful import Resource
from application.models import Questions, Answers, ALL_QUESTIONS
from application.main.checker import question_already_exist, answer_already_exist
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_identity)
from application import models
from application import app
all_answers = list()

MY_QUESTION = models.Questions()
MY_USER = models.Users()

'''question related routes'''


class PostQuestion(Resource):
    @jwt_required
    def post(self):
        '''user can add a question if logged in'''
        identity = get_jwt_identity()
        username = MY_USER.get_user_by_field(key="username", value=identity)
        if username is None:
            return jsonify({"message": "You must be logged in to post"})
        index = 1
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})

        title = data.get('title')
        topic = data.get('topic')
        owner = username
        details = data.get('details')
        question_id = index

        if title is None or not title:
            return jsonify({"message": "Enter title"})
        if details is None or not details:
            return jsonify({"message": "Enter details for your question"})

        response = jsonify(MY_QUESTION.post_question(topic,
                                                     title, details, owner, question_id))
        index += 1
        response.status_code = 200
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
    @jwt_required
    def delete(self, question_id):
        '''delete a question when logged in, method=DELETE'''
        identity = get_jwt_identity()
        username = MY_USER.get_user_by_field(key="username", value=identity)
        if username is None:
            return jsonify({"message": "You must be logged in to delete"})
        response = jsonify(MY_QUESTION.delete(question_id))
        response.status_code = 200

        return response


class PostAnswer(Resource):
    @jwt_required
    def post(self, question_id):
        ''' endpoint for answering a question'''
        identity = get_jwt_identity()
        username = MY_USER.get_user_by_field(key="username", value=identity)
        if username is None:
            return jsonify({"message": "You must be logged in to answer"})
        question = MY_QUESTION.get_single_question(question_id)
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'message': 'Provide an answer'})), 400
        if not question_already_exist(question_id):
            return make_response(jsonify({'message': 'The question' +
                                          ' does not exist'})), 404
        if answer_already_exist(all_answers, 'answer', answer_body):
            return make_response(jsonify(
                {'message': 'This answer is already given'})), 409
        ans_id = str(uuid4())
        answer = Answers(answer_body)
        answer_dict = answer.serialize_answer(
            ans_id, answer, question)
        all_answers.append(answer_dict)
        return make_response(jsonify({'message': 'Answer posted successfully'})), 200


class AcceptAnswer(Resource):
    @jwt_required
    def patch(self, question_id, answer_id):
        '''endpoint to accept an answer as your preffered'''
        identity = get_jwt_identity()
        username = MY_USER.get_user_by_field(key="username", value=identity)
        if username is None:
            return jsonify({"message": "You must be logged in to accept"})
        answer_list = answer_already_exist(all_answers, 'ans_id', answer_id)
        if answer_list:
            if answer_list[0]['accepted']:
                return make_response(jsonify({'message': 'You have' +
                                              'already accepted'})), 409
            answer_list[0]['accepted'] = True
            return make_response(jsonify(
                {'message': 'Succesfully accepted this answer'}
            )), 200
        return make_response(jsonify({'message': 'The answer you are' +
                                      'looking for does not exist'})), 404
