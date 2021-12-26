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
        return item


class MongoPipeline:
    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item