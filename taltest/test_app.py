from abc import ABCMeta
from http import HTTPStatus
import re
from re import _pattern_type as CompiledRegex
import json
import unittest

from flask_testing import TestCase as FlaskTestingTestCase

from tal.api.app_factory import create_app
from tal.api.models import (
    db,
    Post,
    Author,
)


TEST_DATABASE_URI = (
    'postgresql://testrole:testpassword@localhost:5432/theannotatedlifetest'
)


UUID4_REGEX = (
    '[0-9a-f]{8}\-[0-9a-f]{4}\-4[0-9a-f]{3}\-[89ab][0-9a-f]{3}\-[‌​0-9a-f]{12}'
)

BASE_URL_RE = 'http:\/\/[^\/\s]+\/'


class BaseTestCase(FlaskTestingTestCase, metaclass=ABCMeta):

    session = None

    def create_app(self):
        app = create_app()

        # Set up the test config
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_DATABASE_URI
        app.config['TESTING'] = True

        return app

    def setUp(self):
        db.create_all()
        self.session = db.session

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class JsonTestCaseMixin(metaclass=ABCMeta):

    json_types = (
        str,
        int,
        float,
        type(None),
        bool,
        dict,
        list
    )

    def assertIsValidJsonType(self, obj, msg=None):

        self.assertIsInstance(
            obj,
            self.json_types,
            msg
        )

    def assertIsValidExpectedType(self, obj, msg=None):

        self.assertIsInstance(
            obj,
            (*self.json_types, CompiledRegex),
            msg
        )

    def assertFieldMatches(self, value, expected, field_name):

        self.assertIsValidJsonType(
            value,
            f'Field type {type(value)} is not a valid JSON type'
        )

        self.assertIsValidExpectedType(
            expected,
            f'Field type {type(expected)} is not a valid expected type'
        )

        field_type_no_match_msg = (
            f"Field type {type(value)} does not match expected type "
            f"{type(expected)} for field '{field_name}'"
        )

        # We check for each expected type
        if isinstance(expected, dict):

            self.assertIsInstance(
                value,
                type(expected),
                field_type_no_match_msg
            )

            self.assertSequenceEqual(
                value.keys(),
                expected.keys(),
                f"Dictionary keys do not match expected keys for field "
                f"'{field_name}'"
            )

            for subfield, subvalue in value.items():
                self.assertFieldMatches(
                    subvalue,
                    expected[subfield],
                    subfield
                )

        elif isinstance(expected, list):

            self.assertIsInstance(
                value,
                type(expected),
                field_type_no_match_msg
            )

            self.assertEqual(
                len(value),
                len(expected),
                f"List lengths are not equal for field '{field_name}'")

            for idx, el in enumerate(value):
                self.assertFieldMatches(
                    el,
                    expected[idx],
                    field_name
                )

        elif isinstance(expected, CompiledRegex):

            self.assertIsInstance(
                value,
                str,
                field_type_no_match_msg
            )

            # We compare to a regex
            self.assertRegex(
                value,
                expected,
                f"No match for field '{field_name}'"
            )

        else:

            self.assertIsInstance(
                value,
                type(expected),
                field_type_no_match_msg
            )

            self.assertEqual(
                value,
                expected,
                f"Value and expected value not equal for field '{field_name}'"
            )

    def assertResourceMatches(self, payload, expected):

        self.assertIsInstance(
            payload,
            dict,
            'Payload must be a dictionary'
        )

        self.assertIsInstance(
            expected,
            dict,
            'Expected payload must be a dictionary'
        )

        self.assertSequenceEqual(
            payload.keys(),
            expected.keys(),
            'Payload fields do not match expected fields'
        )

        for field, value in payload.items():
            self.assertFieldMatches(
                value,
                expected[field],
                field
            )


class AppTestCase(BaseTestCase):

    def test_root_url(self):
        r = self.client.get('/')
        self.assertStatus(r, HTTPStatus.NOT_FOUND)


class PostRestTestCase(JsonTestCaseMixin, BaseTestCase):

    def test_empty_post_summary_list(self):
        r = self.client.get('/posts/')
        self.assertStatus(r, HTTPStatus.OK)
        self.assertDictEqual(r.json, {'posts': []})

    def test_get_post_summary_list(self):

        # Create three posts
        author_1 = Author(name='test author name')
        author_1.save()

        author_2 = Author(name='test author name 2')
        author_2.save()

        post_data = (
            {
                'title': 'test post 1',
                'date_published': '2017-09-16T17:12:56+00:00',
                'date_written': '2016-09-12T17:12:53+00:00',
                'summary': 'test summary 1',
                'body': 'test body 1',
                'footer': 'test footer 1',
                'author_id': str(author_1.id),
            },
            {
                'title': 'test post 2',
                'date_published': '2017-12-16T17:12:53+00:00',
                'date_written': '2013-07-16T17:12:53+00:00',
                'summary': 'test summary 2',
                'body': 'test body 2',
                'footer': 'test footer 2',
                'author_id': str(author_1.id),
            },
            {
                'title': 'test post 3',
                'date_published': '2014-09-16T17:12:23+00:00',
                'date_written': '2014-11-16T17:11:53+00:00',
                'summary': 'test summary 3',
                'body': 'test body 3',
                'footer': 'test footer 3',
                'author_id': str(author_2.id),
            }
        )

        post_objs = tuple(Post(**post) for post in post_data)

        for post_obj in post_objs:
            post_obj.save()

        # Retrieve the created posts
        expected_responses = {
            'posts': [
                {
                    'id': str(post_objs[idx].id),
                    'url': re.compile(
                        f'^{BASE_URL_RE}posts\/{UUID4_REGEX}\/$'
                    ),
                    'title': post['title'],
                    'date_published': post['date_published'],
                    'date_written': post['date_written'],
                    'summary': post['summary'],
                    'footer': post['footer'],
                    'tags': [],
                    'author_id': post['author_id'],
                    'author': re.compile(
                        f'^{BASE_URL_RE}authors\/{post["author_id"]}\/$'
                    )
                } for idx, post in enumerate(post_data)
            ]
        }

        r = self.client.get('/posts/')
        self.assertStatus(r, HTTPStatus.OK)

        self.assertResourceMatches(r.json, expected_responses)

    def test_get_post_detail(self):

        # Create a post
        author = Author(name='test author name')
        author.save()

        post_data = {
            'title': 'test post',
            'date_published': '2017-09-16T17:12:53+00:00',
            'date_written': '2016-09-16T17:12:53+00:00',
            'summary': 'test summary',
            'body': 'test body',
            'footer': 'test footer',
            'author_id': str(author.id),
        }

        post = Post(**post_data)
        post.save()

        # Retrieve the created post
        expected_response = {
            'id': str(post.id),
            'url': re.compile(f'^{BASE_URL_RE}posts\/{post.id}\/$'),
            'title': post_data['title'],
            'date_published': post_data['date_published'],
            'date_written': post_data['date_written'],
            'body': post_data['body'],
            'footer': post_data['footer'],
            'references': [],
            'tags': [],
            'author_id': post_data['author_id'],
            'author': re.compile(
                f'^{BASE_URL_RE}authors\/{post_data["author_id"]}\/$'
            )
        }

        url = f'/posts/{post.id}/'

        r = self.client.get(url)

        self.assertStatus(r, HTTPStatus.OK)

        self.assertResourceMatches(r.json, expected_response)

    def test_create_post(self):

        # Create an author
        author = Author(name='test author name')
        author.save()

        json_data = {
            'title': 'test post',
            'date_published': '2017-09-16T17:12:53+00:00',
            'date_written': '2016-09-16T17:12:53+00:00',
            'summary': 'test summary',
            'body': 'test body',
            'footer': 'test footer',
            'author_id': str(author.id),
        }

        # Retrieve the created post
        expected_response = {
            'id': re.compile(f'^{UUID4_REGEX}$'),
            'url': re.compile(f'^{BASE_URL_RE}posts\/{UUID4_REGEX}\/$'),
            'title': json_data['title'],
            'date_published': json_data['date_published'],
            'date_written': json_data['date_written'],
            'body': json_data['body'],
            'footer': json_data['footer'],
            'references': [],
            'tags': [],
            'author_id': json_data['author_id'],
            'author': re.compile(
                f'^{BASE_URL_RE}authors\/{json_data["author_id"]}\/$'
            )
        }

        self.assertEqual(self.session.query(Post).count(), 0)

        r = self.client.post('/posts/', data=json.dumps(json_data))
        self.assertStatus(r, HTTPStatus.CREATED)

        self.assertEqual(self.session.query(Post).count(), 1)

        self.assertResourceMatches(r.json, expected_response)


if __name__ == '__main__':
    unittest.main()
