# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с
# заработной платой больше введённой суммы (необходимо анализировать оба поля
# зарплаты).
from pprint import pprint
from gb_db_vacancies import GbDbVacancies


if __name__ == '__main__':
    salary = float(input('Enter salary: '))
    with GbDbVacancies() as vacancies_db:
        for vacancy in vacancies_db.get_vacancies_expensive_more_than(salary):
            pprint(vacancy)
