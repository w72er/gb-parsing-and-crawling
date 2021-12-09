# Вариант I
# Написать программу, которая собирает входящие письма из своего или тестового
# почтового ящика и сложить данные о письмах в базу данных
# (от кого, дата отправки, тема письма, текст письма полный)
from mail_ru_emails_parser import MailRuEmailsParser


if __name__ == '__main__':
    with MailRuEmailsParser() as parser:
        parser.login()
        links = parser.get_all_email_links()
        print(f'len: {len(links)}')
        for link in links[:4]:
            email_id = parser.get_email_id_from_email_url(link)
            email = parser.get_email(link)
            print(f'{email["id"]} {email["date"]} {email["contact"]} {email["subject"][:30]}')
    print('with done')
