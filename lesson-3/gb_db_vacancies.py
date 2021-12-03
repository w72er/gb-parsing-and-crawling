from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GbDbVacancies:
    db_name = 'gb'

    def __init__(self):
        self.client = None
        self.vacancies = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.client = MongoClient('127.0.0.1', 27017)
        db = self.client[self.db_name]
        self.vacancies = db.vacancies

    def close(self):
        # https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        self.client.close()

    def create_indexes(self):
        self.vacancies.create_index('title', unique=True)

    def add(self, vacancies: list):
        for vacancy in vacancies:
            try:
                self.vacancies.insert_one(vacancy)
            except DuplicateKeyError:
                pass  # just ignore duplicated vacancy

    def show(self):
        return self.vacancies.find({})

    def get_vacancies_expensive_more_than(self, salary):
        # return self.vacancies.find({"compensation_min": {"$type": 10}})
        # return self.vacancies.find({"compensation_min": {"$gt": 250000}})
        return self.vacancies.find({
            '$or': [
                {'compensation_min': {'$gt': salary}},
                {'compensation_max': {'$gt': salary}}
            ]
        })
        # [None, None]
        # [None, 10000] max < 10000
        # [10000, None] min < 10000
        # [10000, 20000]



if __name__ == '__main__':
    with GbDbVacancies() as vacancies_db:
        # vacancies_db.vacancies.delete_many({})
        # vacancies_db.create_indexes()
        # vacancies_db.add([{'title': 4, 'a': 'a1', 'b': 'b1'}])
        for vacancy in vacancies_db.show():
            pprint(vacancy)
