from flask import Flask
from ..instance import app_config
from flask_restful import Api


def create_app(config_name):
    from application import (
        PostQuestion, PostAnswer, GetAllQuestions, GetSingleQuestion, DeleteQuestion, AcceptAnswer)

    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    api = Api(app)

    api.add_resource(PostQuestion, '/api/v1/questions')
    api.add_resource(GetAllQuestions, '/api/v1/questions')
    api.add_resource(GetSingleQuestion, '/api/v1/questions/<int:question_id>')
    api.add_resource(DeleteQuestion, '/api/v1/questions/<int:question_id>')
    api.add_resource(PostAnswer, '/api/v1/questions/<int:question_id>/answers')
    api.add_resource(
        AcceptAnswer, '/api/v1/questions/<int:question_id>/answers/<answer_id>')
    return app
