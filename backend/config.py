import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.urandom(32)


class DevelopmentConfig(Config):
    DEBUG = True
    database_name = "trivia"
    database_path = "postgresql://{}/{}".format("localhost:5432", database_name)
    SQLALCHEMY_DATABASE_URI = database_path

class TestingConfig(Config):
    TESTING = True
    database_name = "trivia_test"
    database_path = "postgresql://{}/{}".format("localhost:5432", database_name)
    SQLALCHEMY_DATABASE_URI = database_path

app_config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig
}

FLASK_DEBUG = os.environ.get('FLASK_DEBUG', False)
