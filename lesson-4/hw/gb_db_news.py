from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GbDbNews:
    db_name = 'gb'

    def __init__(self):
        self.client = None
        self.news = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.client = MongoClient('127.0.0.1', 27017)
        db = self.client[self.db_name]
        self.news = db.news

    def close(self):
        # https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        self.client.close()

    def create_indexes(self):
        self.news.create_index('link', unique=True)

    def mongodbfy_news(self, news):
        n = dict(news)
        d = n['published_at']
        dt = datetime.combine(d, datetime.min.time())
        n['published_at'] = dt.timestamp()

        return n

    def add(self, news_list: list):
        for n in news_list:
            try:
                self.news.insert_one(self.mongodbfy_news(n))
            except DuplicateKeyError:
                pass  # just ignore duplicated news

    def pythonyfy(self, mongo_news):
        news = dict(mongo_news)
        news['published_at'] = datetime.fromtimestamp(news['published_at']).date()
        return news

    def show(self):
        mongo_news = self.news.find({})
        return map(self.pythonyfy, mongo_news)


if __name__ == '__main__':
    with GbDbNews() as news_db:
        for n in news_db.show():
            pprint(n)
