import re
from flask import Flask, request, jsonify, make_response
from flask_restful import Resource
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_identity)
from application.models import Question, Answer
from application.main.checker import question_already_exist, answer_already_exist
from application import app


'''question related routes'''


def dictionary(a_list):
    """Get an item from a list"""
    for i in a_list:
        return i


class PostQuestion(Resource):
    @jwt_required
    def post(self):
        '''user can add a question if logged in'''
        identity = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})

        title = data.get('title')
        topic = data.get('topic')
        owner = identity
        details = data.get('details')

        if title is None or not title:
            return jsonify({"message": "Enter title"})
        if details is None or not details:
            return jsonify({"message": "Enter details for your question"})
        if owner is None:
            return jsonify({"message": "You must be logged in to post"})

        questions = Question(
            title,
            topic,
            details,
            owner=identity
        )
        questions.insert()
        response = {"message": "Question posted successfully"}

        return response, 201


class GetAllQuestions(Resource):
    def get(self):
        ''' get all questions method="GET"'''
        get_questions = Question.get_all()
        if get_questions == []:
            return {"message": "Currently no questions in database"}, 404
        response = {"total": len(get_questions),
                    "questions": get_questions}, 200

        return response


class GetSingleQuestion(Resource):
    def get(self, question_id):
        '''endpoint to get question by id'''
        get_question = Question.get_single_question(question_id)
        response = {"question": get_question}, 200
        return response


class DeleteQuestion(Resource):
    @jwt_required
    def delete(self, question_id):
        '''delete a question when logged in, method=DELETE'''
        identity = get_jwt_identity()

        if identity is None:
            return jsonify({"message": "You must be logged in to delete"})
        question = Question.get_item_by_id(question_id)
        if question['owner'] != get_jwt_identity():
            return{"message": "You are not allowed to delete this question"}
        Question.delete(question_id)

        return {"message": "Question deleted successfully"}, 200


class PostAnswer(Resource):
    @jwt_required
    def post(self, question_id):
        ''' endpoint for answering a question'''
        identity = get_jwt_identity()
        if identity is None:
            return jsonify({"message": "You must be logged in to answer"})
        question = Question.get_single_question(question_id)
        answer_body = request.json.get('answer')
        if not answer_body:
            return make_response(jsonify({'message': 'Provide an answer'})), 400
        if not question_already_exist(question_id):
            return make_response(jsonify({'message': 'The question' +
                                          ' does not exist'})), 404
        answers = Answer.get_one_by_field('answer', answer_body)

        if answers is not None:
            return {"message": "This answer is already given"}, 409

        answer = Answer(answer_body,
                        owner=identity,
                        question=question['id']
                        )
        answer.insert()
        question['answers'] += 1
        Question.update('answers', question['answers'], question_id)
        return {'message': 'Answer posted successfully'}, 200


class GetAllAnswers(Resource):

    @jwt_required
    def get(self, question_id):
        """Gets all the answers for this particular question"""
        question_already_exist(question_id)
        question = Question.get_item_by_id(question_id)
        data = Answer.get_all()
        answers = [answer for answer in data
                   if answer['question'] == question['id']]
        if answers == []:
            return {"message": "No answers for this question"}, 404
        response = {
            'total': len(answers),
            'data': answers
        }
        return response, 200


class AcceptAnswer(Resource):

    @jwt_required
    def patch(self, question_id, answer_id):
        '''endpoint to accept an answer as your preffered'''
        identity = get_jwt_identity()
        if identity is None:
            return jsonify({"message": "You must be logged in to accept"})
        allquestions = Question.get_all()
        allanswers = Answer.get_all()
        questions = [quiz for quiz in allquestions
                     if quiz['owner'] == get_jwt_identity()]
        answers = [answer for answer in allanswers
                   if answer['question'] == dictionary(questions)['id']]
        if answers == []:
            return {"message": "No answers for this question"}, 404

        answer_list = answer_already_exist(allanswers, 'ans_id', answer_id)
        if answer_list:
            for ans in answers:
                if ans['accepted'] != False:
                    return {"message": "Answer already accepted"}, 400
                elif ans['id'] == answer_id \
                        and ans['question'] == question_id:
                    ans['accepted'] = True
                    Answer.update('accepted', ans['accepted'], answer_id)
                    return {"message": "Answer accepted"}, 200
        return {'message': 'The answer you are' +
                'looking for does not exist'}, 404


class GetUserQuestions(Resource):
    def get(self):
        """Get all questions for current user"""
        data = Question.get_all()
        myquiz = [qns for qns in data
                  if qns['owner'] == get_jwt_identity()]
        if myquiz == []:

            return {"message": "You haven't asked any questions"}, 404
        response = {
            'total': len(myquiz),
            'data': myquiz
        }
        return response, 200
