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
        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.process_salary_hhru(item['salary'])
            item['_id'] = 'hhru: ' + item['link'].split('?')[0].split('/')[-1]
        elif spider.name == 'superjobru':
            item['min'], item['max'], item['cur'] = self.process_salary_superjobru(item['salary'])
            item['_id'] = 'superjobru: ' + item['link'].split('/')[-1]
        del item['salary']

        collection = self.mongobase[spider.name]
        collection.insert_one(dict(item))
        return item

    @staticmethod
    def transform_salary(salary: str) -> int:
        return int(salary.replace('\xa0', ''))

    def process_salary_superjobru(self, salary):
        # ['от', '\xa0', '360\xa0000\xa0руб.', '/', 'месяц']
        # ['до', '\xa0', '150\xa0000\xa0руб.', '/', 'месяц']
        # ['По договорённости']
        # ['30\xa0000', '\xa0', '—', '\xa0', '35\xa0000', '\xa0', 'руб.', '/', 'месяц']
        if salary[0] == 'По договорённости':
            return None, None, None

        if salary[0] == 'от':
            frm = int(str.join('', salary[2].split('\xa0')[:-1]))
            cur = salary[2].split('\xa0')[-1]
            return frm, None, cur

        if salary[0] == 'до':
            to = int(str.join('', salary[2].split('\xa0')[:-1]))
            cur = salary[2].split('\xa0')[-1]
            return None, to, cur

        if salary[2] == '—':
            return self.transform_salary(salary[0]), self.transform_salary(salary[4]), salary[6]
            return salary[1], None, salary[3]
        pass

    def process_salary_hhru(self, salary):
        if salary[0] == 'з/п не указана':
            return None, None, None

        if salary[2] == ' до ':
            return self.transform_salary(salary[1]), self.transform_salary(salary[3]), salary[5]

        if salary[0] == 'от ':
            return self.transform_salary(salary[1]), None, salary[3]

        if salary[0] == 'до ':
            return None, self.transform_salary(salary[1]), salary[3]

        return None, None, None
