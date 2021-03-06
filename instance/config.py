class Config(object):
    '''parent config file'''
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
   


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
