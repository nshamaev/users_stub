import unittest
import json
from . import app
from sys import maxsize
from pymongo import MongoClient
from users_stub.stub_data import insert_users


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = app.app.test_client()
        self.client = MongoClient('db')
        self.users_database = self.client.test_users
        self.users = self.users_database.users
        insert_users(self.users_database)

    def test_get_by_id(self):
        for user in self.users.find({}, {"_id": False}):
            result = self.app.get('/users/%d' % user['id'])
            self.assertEqual(json.loads(result.data), user)
            self.assertEqual(result.status_code, 200)

    def test_invalid_id(self):
        result = self.app.get('/users/' + str(maxsize + 1))
        self.assertEqual(result.status_code, 400)

        result = self.app.get('/users/' + str(-2 - maxsize))
        self.assertEqual(result.status_code, 400)

        result = self.app.get('/users/!@#$%^&*()')
        self.assertEqual(result.status_code, 400)

        result = self.app.get('/users/user_id')
        self.assertEqual(result.status_code, 400)\

        result = self.app.get('/users/1.5')
        self.assertEqual(result.status_code, 400)

    def test_non_exits_id(self):
        result = self.app.get('/users/9999')
        self.assertEqual(result.status_code, 404)

        result = self.app.get('/users/' + str(maxsize))
        self.assertEqual(result.status_code, 404)

        result = self.app.get('/users/' + str(-maxsize))
        self.assertEqual(result.status_code, 404)

        result = self.app.get('/users/0')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        self.client.drop_database('test_users')