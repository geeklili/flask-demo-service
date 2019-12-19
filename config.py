import os
import logging


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_REDIRECT = False
    JSON_AS_ASCII = False

    MONGO_URI = os.getenv('MONGO_JD_ALI_URI')
    MYSQL_URI = os.getenv('MYSQL_DATABASE_URI')
    MYSQL_OUT_URI = os.getenv('MYSQL_DATABASE_OUT_URI')
    MONGO_JD_ALI_URI = os.getenv('MONGO_JD_ALI_URI')

    PROPAGATE_EXCEPTIONS = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class UATConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        app.logger.setLevel(logging.INFO)


class ProductionConfig(Config):
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        app.logger.setLevel(logging.INFO)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': UATConfig
}


