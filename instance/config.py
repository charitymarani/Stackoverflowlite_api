class Config(object):
    '''parent config file'''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET_KEY = 'very secret'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access']


class DevelopmentConfig(Config):
    '''Configurations for development'''
    Debug = True


class TestingConfig(Config):
    '''configurations for testing with a separate test database'''
    TESTING = True
    Debug = True
    SECRET_KEY = 'topmost-secret'


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
