from pprint import pprint
from pymongo import MongoClient


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
        self.users.update_one(
            {'_id': user['_id']},
            {'$set': {"_id": user['_id'], "username": user['username'], "photo": user['photo'],
                      "following": [], "followers": []}},
            upsert=True)

    def get_all(self):
        return self.users.find({})

    def get_followings(self, user_id):
        """ На кого я подписан """
        return self.users.find({'following': {'$in': [user_id]}})

    def add_followings_to_user(self, user_id, following_ids):
        self.users.update_many(
            {'_id': {'$in': following_ids}},
            {'$push': {'following': user_id}}
        )

    def get_followers(self, user_id):
        """ На кого я подписан """
        return self.users.find({'followers': {'$in': [user_id]}})

    def add_followers_to_user(self, user_id, follower_ids):
        self.users.update_many(
            {'_id': {'$in': follower_ids}},
            {'$push': {'followers': user_id}}
        )


if __name__ == '__main__':
    with UsersDb() as users_db:
        users_db.users.drop()

        users_db.add({"_id": "1", "username": "Ivan Petrov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})
        users_db.add({"_id": "2", "username": "Petr Suvorov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})
        users_db.add({"_id": "3", "username": "Sidr Ivanov", "photo": "https://insta.com/photos/2A39BC328E.jpeg"})

        # 1 пользователь подписан на 2 и 3
        # 2 пользователь подписан на 3
        # 3 пользователь подписан на 2 и 1
        users_db.add_followings_to_user('1', ['2', '3'])
        users_db.add_followings_to_user('2', ['3'])
        users_db.add_followings_to_user('3', ['1', '2'])

        # на пользователя 1 подписались 2
        # на пользователя 2 подписались 1, 3
        # на пользователя 3 подписались []
        users_db.add_followers_to_user('1', ['2'])
        users_db.add_followers_to_user('2', ['1', '3'])
        users_db.add_followers_to_user('3', [])

        # users_db.add({
        #     "_id": "1", "username": "Ivan Petrov", "photo": "https://insta.com/photos/2A39BC328E.jpeg",
        #     "following": [3],
        #     "followers": [2]})
        # users_db.add({
        #     "_id": "2", "username": "Petr Suvorov", "photo": "https://insta.com/photos/2A39BC328E.jpeg",
        #     "following": [1, 3],
        #     "followers": [1]})
        # users_db.add({
        #     "_id": "3", "username": "Sidr Ivanov", "photo": "https://insta.com/photos/2A39BC328E.jpeg",
        #     "following": [1, 2],
        #     "followers": [2]})

        # for user in users_db.get_all():
        #     pprint(user)

        for user in users_db.get_followers('1'):
            pprint(user)
