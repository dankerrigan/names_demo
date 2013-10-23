__author__ = 'dankerrigan'

from riakjson.client import Client
from riakjson.query import Query
from riakjson.query import ASCENDING, eq


class UserData(object):
    def __init__(self):
        self.client = Client()
        self.users = self.client.users

    def user_favorites(self, username):
        q = Query(eq('username', username))
        q.sort({'name', ASCENDING})

        result = self.users.find(q.build())

        return list(result)

    def add_user_favorite(self, username, name):
        self.users.insert({'username': username, 'name': name})