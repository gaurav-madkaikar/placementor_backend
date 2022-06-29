import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = 'sasds9wn'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URI') or \
        'mysql+pymysql://root:@localhost/flask_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    HOST = '127.0.0.1'
    PORT = 5000
    SQLALCHEMY_DATABASE_URI = os.getenv("TESTING_DATABASE_URI") or \
        'mysql+pymysql://root:@localhost/flask_test'
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True