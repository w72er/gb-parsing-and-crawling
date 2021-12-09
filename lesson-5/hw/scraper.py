# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
from mail_ru_emails_parser import MailRuEmailsParser
from gb_db_emails import GbDbEmails


if __name__ == '__main__':
    with MailRuEmailsParser() as parser, GbDbEmails() as emails_db:
        emails_db.create_indexes()
        parser.login()
        links = parser.get_all_email_links()
        for link in links:
            email_id = parser.get_email_id_from_email_url(link)
            if not emails_db.has_email(email_id):
                email = parser.get_email(link)
                emails_db.add([email])
                print(f'{email["id"]} {email["date"]} {email["contact"]} {email["subject"][:30]}')
