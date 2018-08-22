import re
from flask import Flask, request, jsonify, make_response, render_template
from flask_restful import Resource
from application.main.current_user import get_logged_in_user
from application.models import Questions, Answers
from application.main.checker import question_already_exist, answer_already_exist
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_identity)
from application import models
from application.main.validate import Validate
from application.models import ALL_QUESTIONS, USERS
from application import blacklist
all_answers = list()


MY_QUESTION = models.Questions()
MY_USER = models.Users()


class Register(Resource):
    def post(self):
        '''endpoint to register a user'''
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})
        username = data.get("username")
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        if not username or not name or not email or not password or not confirm_password:
            return dict(message="name, username, email," +
                        "password or confirm_password fields missing"), 400
        v = Validate().validate_register(username, name, email, password, confirm_password)
        if "message" in v:
            return v, 400
        if username in USERS:
            return {"message": " Username already exists"}, 409
        response = jsonify(MY_USER.put(name=v["name"], username=v["username"],
                                       email=v["email"], password=v["password"]))
        response.status_code = 201
        return response


class Login(Resource):
    def post(self):
        '''login user by verifying password and creating an access token'''
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})
        username = data.get('username')
        password = data.get('password')
        auth = MY_USER.verify_password(username, password)

        if auth == "True":
            access_token = create_access_token(identity=username)
            return dict(
                token=access_token,
                message="Login successful"), 200

        response = jsonify(auth)
        response.status_code = 401
        return response


class Logout(Resource):
    @jwt_required
    def post(self):
        '''logout user by revoking password'''
        json_token_identifier = get_raw_jwt()['jti']
        blacklist.add(json_token_identifier)
        return {"message": "Successfully logged out"}, 200


class Reset_password(Resource):
    def post(self):
        '''reset user password'''
        data = request.get_json()
        if not data:
            return jsonify({"message": "Fields cannot be empty"})
        username = data.get("username")
        if not username:
            return {"message": "Enter username"}, 400

        response = jsonify(MY_USER.reset_password(username))
        response.status_code = 200
        return response
