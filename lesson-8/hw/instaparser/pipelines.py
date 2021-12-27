# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from users_db import UsersDb
from pprint import pprint


class InstaparserPipeline:
    def process_item(self, item, spider):
        with UsersDb() as users_db:
            user_a = item['user_a']
            users_db.add(user_a)
            for following_user in item['following_users']:
                users_db.add(following_user)
                users_db.add_followings_to_user(user_a['_id'], [following_user['_id']])

            for follower_user in item['follower_users']:
                users_db.add(follower_user)
                users_db.add_followers_to_user(user_a['_id'], [follower_user['_id']])
        return item
