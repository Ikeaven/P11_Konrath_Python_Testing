import os


basedire = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something_special'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE = os.path.join(basedire, 'data')
    MAX_PLACES = 12


class TestingConfig(Config):
    TESTING = True
    DATABASE = os.path.join(basedire, 'data_test')
    MAX_PLACES = 600


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE = os.path.join(basedire, 'data')
    MAX_PLACES = 12


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
