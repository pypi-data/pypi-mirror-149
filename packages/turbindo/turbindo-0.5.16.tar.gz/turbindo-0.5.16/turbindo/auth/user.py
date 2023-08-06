import json
from box import Box
from turbindo.database.default.classes import User as DBUser


class User(object):
    def __init__(self, name: str, organizaion: str, admin: bool, tags: list):
        self.data = Box({
            "name": name,
            "organizaion": organizaion,
            "admin": admin,
            "tags": tags
        })

    @staticmethod
    def from_dbuser(dbuser: DBUser):
        return User(dbuser.name, dbuser.tennant, dbuser.admin, [dbuser.role])

    def __str__(self):
        return json.dumps(self.data)

    @property
    def name(self):
        return self.data.name

    @property
    def organizaion(self):
        return self.data.organizaion

    @property
    def admin(self):
        return self.data.admin

    @property
    def tags(self) -> list:
        return self.data.tags
