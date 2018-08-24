import string
import random
from werkzeug.security import generate_password_hash, check_password_hash
'''models.py containing models for the API'''
blacklist = {}


class Users(object):
    """Creates the user model"""

    def __init__(self, name, username, email, password):
        """Initializes the user model"""

        self.name = name
        self.username = username
        self.email = email
        pw_hash = generate_password_hash(
            password).decode('utf-8')
        self.password = pw_hash

    def verify_password(self, password):
        """Verify that the hashed password matches the user input password"""
        return check_password_hash(self.password, password)


class Questions(object):
    """Question model"""

    def __init__(self, topic=None, title=None,
                 details=None, owner=None, answers=0):
        self.topic = topic
        self.title = title
        self.details = details
        self.owner = owner
        self.answers = answers


class Answers(object):
    """The answer model"""

    def __init__(self, answer=None,
                 owner=None, question=None):
        self.answer = answer
        self.accepted = False
        self.owner = owner
        self.question = question


class BlackListToken(object):
    """Creates the blacklisting model"""

    def __init__(self, jti):
        """Initializes the blacklist model"""
        self.jti = jti

    @classmethod
    def check_blacklist(cls, auth_token):
        """Check if the token is blacklisted"""
        res = cls.get_by_field(key='jti', value=auth_token)
        return bool(res)

    @classmethod
    def get_by_field(cls, key, value):
        if blacklist is None:
            return {}
        for item in blacklist.values():
            if item[key] == value:
                return item
