from flask import Flask
from flask_jwt_extended import JWTManager
from instance import app_config
from flask_restful import Api

blacklist = set()


def create_app(config_name):
    from application import (
        PostQuestion, PostAnswer, GetAllQuestions, GetSingleQuestion, DeleteQuestion, AcceptAnswer, Register, Login, Logout, Reset_password)

    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')
    jwt = JWTManager(app)
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    api = Api(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        json_token_identifier = decrypted_token['jti']
        return json_token_identifier in blacklist

    api.add_resource(Register, '/api/v1/auth/register')
    api.add_resource(Login, '/api/v1/auth/login')
    api.add_resource(Logout, '/api/v1/auth/logout')
    api.add_resource(Reset_password, '/api/v1/auth/reset_password')
    api.add_resource(PostQuestion, '/api/v1/questions')
    api.add_resource(GetAllQuestions, '/api/v1/questions')
    api.add_resource(GetSingleQuestion, '/api/v1/questions/<int:question_id>')
    api.add_resource(DeleteQuestion, '/api/v1/questions/<int:question_id>')
    api.add_resource(PostAnswer, '/api/v1/questions/<int:question_id>/answers')
    api.add_resource(
        AcceptAnswer, '/api/v1/questions/<int:question_id>/answers/<answer_id>')
    return app
