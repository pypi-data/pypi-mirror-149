import contextlib
from collections import OrderedDict
from pprint import pprint
from typing import Type

import django.contrib.auth.models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import connection
from django.test import TestCase as __TestCase
from django.test.utils import CaptureQueriesContext
from rest_framework.response import Response
from rest_framework.test import APIClient

user_model: Type[django.contrib.auth.models.AbstractUser] = get_user_model()


class TestCase(__TestCase):
    """
    Define a simpler test flow by omit some repeatable works.
    The examples can be find at the app ``blog``.
    """

    @contextlib.contextmanager
    def print_queries(self):
        with CaptureQueriesContext(connection) as ctx:
            yield
            for query in ctx.captured_queries:
                print(query['sql'])

    def setUp(self) -> None:
        self.client = APIClient()
        self.admin_user: user_model = user_model.objects.create_superuser(
            username='test-user', password='test-password')
        self.normal_user: user_model = user_model.objects.create_user(
            username='normal-user', password='test-password')
        self.anonymous_user = AnonymousUser()
        super().setUp()

    def login_with_admin(self):
        self.client.force_authenticate(self.admin_user)

    def login_with_normal(self):
        self.client.force_authenticate(self.normal_user)

    def logout(self):
        self.client.force_authenticate()

    def assert_response(self, response: Response, status_code: int, *test_groups):
        try:
            self.assertEqual(response.status_code, status_code)
            if test_groups:
                if not isinstance(test_groups[0], tuple):
                    test_groups = (test_groups,)
                for args in test_groups:
                    d = response.data
                    for key in args[:-1]:
                        if isinstance(d, (dict, OrderedDict)):
                            self.assertIn(key, d)
                        d = d[key]
                    self.assertEqual(d, args[-1])
            return response
        except AssertionError:
            pprint(response.data)
            raise

    def assert_get(self, path: str, data, status_code: int, *groups):
        return self.assert_response(self.client.get(path, data), status_code, *groups)

    def assert_post(self, path: str, data, status_code: int, *groups):
        return self.assert_response(self.client.post(path, data, format='json'), status_code, *groups)

    def assert_patch(self, path: str, data, status_code: int, *groups):
        return self.assert_response(self.client.patch(path, data, format='json'), status_code, *groups)

    def assert_delete(self, path: str, data, status_code: int, *groups):
        return self.assert_response(self.client.delete(path, data), status_code, *groups)


class AdminTestCase(TestCase):
    def setUp(self) -> None:
        super(AdminTestCase, self).setUp()
        self.login_with_admin()
