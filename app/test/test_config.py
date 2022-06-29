import os
import unittest

from flask import current_app
from flask_testing import TestCase

from app.config import basedir
from app import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] == os.getenv("SECRET_KEY"))
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        # self.assertTrue(
        #     app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv('DATABASE_URI')
        # )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('app.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] == '')
        self.assertTrue(app.config['DEBUG'])
        # self.assertTrue(
        #     app.config['SQLALCHEMY_DATABASE_URI'] == os.getenv(
        #         'TESTING_DATABASE_URI')
        # )



if __name__ == '__main__':
    unittest.main()
