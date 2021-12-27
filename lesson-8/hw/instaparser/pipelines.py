# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from users_db import UsersDb


class InstaparserPipeline:
    def process_item(self, item, spider):
        with UsersDb() as users_db:
            user_a = item['user_a']
            users_db.add(user_a)
            users_db.add_relation(user_a, item['following_users'], 'following')
            users_db.add_relation(user_a, item['follower_users'], 'followers')
        return item
