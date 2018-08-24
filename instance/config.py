"""
Imports
"""
import os
DATABASE_URL = os.getenv('DATABASE_URL')


class Config(object):
    '''parent config file'''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'very secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']
    SECRET_KEY = 'HACHoooaadsf8960-38-(* & ^W(*kdfll'
    DATABASE_URI = 'postgresql://postgres:chamaro68@localhost:5432/stackoverflow'


class DevelopmentConfig(Config):
    '''Configurations for development'''
    Debug = True


class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    Debug = True
    DATABASE_URI = 'postgresql://postgres:chamaro68@localhost:5432/testdb'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
