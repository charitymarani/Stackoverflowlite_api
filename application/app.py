import os
import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
from flask import Flask
from flask_jwt_extended import JWTManager
from ..instance import app_config, DATABASE_URL
from flask_restful import Api
from ..application.models.models import BlackList

blacklist = set()


def database_config(db_url):
    """This creates the database configuration"""
    url = urlparse(db_url)

    if os.environ.get('DATABASE_URL'):
        database_uri = os.environ.get('DATABASE_URL')

    config = dict(
        dbname=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return config


class Database:
    """Connecting to the database"""

    def __init__(self, conf):
        self.config = database_config(conf)

    def init_db(self):
        """Initializes the database"""
        self.connection = psycopg2.connect(**self.config)
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
        self.connection.close()


db = Database(DATABASE_URL)


def create_app(config_name):
    from .views.questions import (
        PostQuestion, PostAnswer, GetAllQuestions, GetSingleQuestion, DeleteQuestion, AcceptAnswer, GetUserQuestions, GetAllAnswers)
    from.views.users import (Register, Login, Logout, Reset_password)
    app = Flask(__name__, template_folder='./templates',
                static_folder='./static')
    jwt = JWTManager(app)
    db.init_db()
    app.config.from_object(app_config[config_name])
    app.url_map.strict_slashes = False
    api = Api(app)

    @jwt.user_identity_loader
    def user_identity_lookup(user_object):
        '''set token identity from user_object passed'''
        return user_object.username

    @jwt.token_in_blacklist_loader
    def check_if_token_blacklist(decrypted_token):
        '''check if jti(unique identifier) is in black list'''
        jti = decrypted_token['jti']
        return BlackList.get_one_by_field(field='jti', value=jti) is not None

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
    api.add_resource(GetUserQuestions, '/api/v1/questions/myquestions')
    api.add_resource(
        GetAllAnswers, '/ api/v1/questions/<int:question_id>/answers')
    return app
