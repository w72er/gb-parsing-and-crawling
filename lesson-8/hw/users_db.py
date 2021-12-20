
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class UsersDb:
    db_name = 'gb'

    def __init__(self):
        self.client = None
        self.users = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.client = MongoClient('127.0.0.1', 27017)
        db = self.client[self.db_name]
        self.users = db.users

    def close(self):
        # https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        self.client.close()

    def add(self, user):
        # find_by_user_id = {'_id': user['_id']}
        # self.users.update_one(find_by_user_id, {'$set': user})
        self.users.insert_one(user)
        # todo: а как добавить подписчика, если перезаписывать?

    def get_all(self):
        return self.users.find({})

    def get_followers(self, user_id):
        return self.users.find({'following'})


if __name__ == '__main__':
    with UsersDb() as users_db:
        users_db.users.drop()

        users_db.add({"_id": "1", "name": "Ivan Petrov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})
        users_db.add({"_id": "2", "name": "Petr Sidorov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})
        users_db.add({"_id": "3", "name": "Sidr Ivanov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})

        for user in users_db.get_all():
            pprint(user)
