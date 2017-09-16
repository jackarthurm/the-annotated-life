from abc import ABCMeta
from http.client import (
    OK,
    NOT_FOUND
)

import unittest

from flask_testing import TestCase as FlaskTestingTestCase

from tal.api.app_factory import create_app
from tal.api.models import db


TEST_DATABASE_URI = (
    'postgresql://testrole:testpassword@localhost:5432/theannotatedlifetest'
)


class BaseTestCase(FlaskTestingTestCase, metaclass=ABCMeta):

    def create_app(self):
        app = create_app()

        # Set up the test config
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        app.config['TESTING'] = True

        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class AppTestCase(BaseTestCase):

    def test_root_url(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, NOT_FOUND)


class PostRestTestCase(BaseTestCase):

    def test_empty_post_summary_list(self):
        r = self.client.get('/posts/')
        self.assertEqual(r.status_code, OK)
        self.assertDictEqual(r.json, {'posts': []})


if __name__ == '__main__':
    unittest.main()
