import os
import unittest

from flask import current_app, Flask
from flask_testing import TestCase


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('app.main.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):

        self.assertFalse(
            current_app.config['SECRET_KEY'] == 'this-is-fake')
        self.assertTrue(current_app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)


class TestTestingConfig(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('app.main.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(
            current_app.config['SECRET_KEY'] == 'this-is-fake')
        self.assertTrue(current_app.config['DEBUG'] is True)


class TestProductionConfig(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('app.main.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(current_app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()
