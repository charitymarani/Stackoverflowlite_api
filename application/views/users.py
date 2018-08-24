import re
import random
import string
from flask import Flask, request, jsonify, make_response, render_template
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_raw_jwt, get_jwt_identity)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Resource
from application.main.current_user import get_logged_in_user
from application.models import Questions, Answers, User, Blacklist
from application.main.checker import question_already_exist, answer_already_exist
from application import models
from application.main.validate import Validate
from application import blacklist


class Register(Resource):

    '''Register a user'''

    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 400
        username = data.get('username')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not username or not name or not email or not password or not confirm_password:
            return dict(message="name, username, email, password or confirm_password fields missing"), 400
        v = Validate().validate_register(username, name, email, password, confirm_password)
        if "message" in v:
            return v, 400

        if User.get_user_by_username(v["username"]):
            return {"message": "Add user failed. Username already exists"}, 409
        if User.get_user_by_email(v["email"]):
            return {"message": "Add user failed. Email entered already exists"}, 409

        my_user = User(username=v["username"], name=v["name"],
                       email=v["email"], password=v["password"])
        my_user.update()
        return {"message": "User successfully added"}, 201


class Login(Resource):
    '''login user by verifying password and creating an access token'''

    def post(self):
        '''method ['POST']'''
        data = request.get_json()
        if not data:
            return {"message": "Fields cannot be empty"}, 400
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {"message": "Username or password missing"}, 400

        user_object = User.get_user_by_username(username)
        if user_object is None:
            return {"message": "Incorrect username"}, 401

        if check_password_hash(user_object.password, password) is True:
            access_token = create_access_token(identity=user_object)
            user_object.update()
            return dict(message="Login successful", token=access_token), 200

        return {"message": "Incorrect password"}, 401


class Logout(Resource):
    @jwt_required
    def post(self):
        '''logout user by revoking token'''
        json_token_identifier = get_raw_jwt()['jti']

        revoked_token = Blacklist(
            json_token_identifier=json_token_identifier)
        revoked_token.update()
        return {"message": "Successfully logged out"}, 200


class Reset_password(Resource):

    def post(self):
        '''Reset a password'''
        data = request.get_json()
        if not data:
            return {"message": "Enter username"}, 400
        username = data.get('username')
        if not username:
            return {"message": "Enter username"}, 400
        user = User.get_user_by_username(username)
        if user is not None:
            generated_password = ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

            user.reset_password = generate_password_hash(generated_password)
            user.update()
            reset_token = create_access_token(identity=user)
            return dict(reset_token=reset_token, reset_password=generated_password), 200

        return {"message": "User doesn't exist"}, 404
