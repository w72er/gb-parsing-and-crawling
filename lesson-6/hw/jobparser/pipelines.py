# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.lesson6hw

    def process_item(self, item, spider):
        item['min'], item['max'], item['cur'] = self.process_salary(item['salary'])
        # del item['salary']
        # if spider.name == 'sjru':

        collection = self.mongobase[spider.name]
        collection.insert_one(dict(item))
        return item

    @staticmethod
    def transform_salary(salary: str) -> int:
        return int(salary.replace('\xa0', ''))

    @staticmethod
    def process_salary(salary):
        if salary[0] == 'з/п не указана':
            return None, None, None

        if salary[2] == ' до ':
            return salary[1], salary[3], salary[5]

        if salary[0] == 'от ':
            return salary[1], None, salary[3]

        if salary[0] == 'до ':
            return salary[1], None, salary[3]

        return None, None, None
