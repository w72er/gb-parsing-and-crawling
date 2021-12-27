# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from users_db import UsersDb


class InstaparserPipeline:
    def __init__(self):
        self.users_db = UsersDb()

    def open_spider(self, spider):
        self.users_db.open()

    def close_spider(self, spider):
        self.users_db.close()

    def process_item(self, item, spider):
        user_a = item['user_a']
        self.users_db.add(user_a)
        self.users_db.add_relation(user_a, item['following_users'], 'following')
        self.users_db.add_relation(user_a, item['follower_users'], 'followers')
        return item
