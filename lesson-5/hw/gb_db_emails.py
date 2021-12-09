from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


class GbDbEmails:
    db_name = 'gb'

    def __init__(self):
        self.client = None
        self.emails = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def open(self):
        self.client = MongoClient('127.0.0.1', 27017)
        db = self.client[self.db_name]
        self.emails = db.emails

    def close(self):
        # https://stackoverflow.com/questions/20613339/close-never-close-connections-in-pymongo
        self.client.close()

    def create_indexes(self):
        self.emails.create_index('id', unique=True)

    def add(self, emails: list):
        for email in emails:
            try:
                self.emails.insert_one(email)
            except DuplicateKeyError:
                pass  # just ignore duplicated email

    def get_all_emails(self):
        return self.emails.find({})

    def has_email(self, id: str) -> bool:
        return self.emails.count_documents({'id': id}) != 0


if __name__ == '__main__':
    with GbDbEmails() as emails_db:
        # emails_db.emails.drop()
        # # emails_db.emails.delete_many({})
        # emails_db.create_indexes()
        # emails_db.add([{'id': '1'}])
        # emails_db.add([{'id': '1'}])
        # emails_db.add([{'id': '2'}])
        # emails_db.has_email('2')
        for email in emails_db.get_all_emails():
            print(f'{email["id"]} {email["date"]} {email["contact"]} {email["subject"][:30]}')
