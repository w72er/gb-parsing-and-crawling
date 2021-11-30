from parse_hh_ru_vacancies import parse_hh_ru_vacancies
from pandas import json_normalize
from gb_db_vacancies import GbDbVacancies

vacancies_csv = 'vacancies.csv'


if __name__ == '__main__':
    job_title = input('Enter job title: ')
    page_count = int(input('Enter the page count from which you want to parse vacancies: '))
    print(job_title, page_count)

    vacancies = parse_hh_ru_vacancies(job_title, page_count)

    with GbDbVacancies() as vacancies_db:
        vacancies_db.create_indexes()  # if you want you can place it to another place.
        vacancies_db.add(vacancies)

    df = json_normalize(vacancies)
    print(df.head())
    print(df.columns)
    df.to_csv(vacancies_csv, index=False)
