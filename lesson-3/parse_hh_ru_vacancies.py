import requests
from bs4 import BeautifulSoup, element
import re


def parse_hh_ru_vacancies(job_title: str, page_count: int) -> list:
    url = 'https://novosibirsk.hh.ru/search/vacancy'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    page_number = 1
    vacancies = []
    while True:
        params = {
            'area': 4,
            'fromSearchLine': 'true',
            'text': job_title}
        # the page number starts from zero
        if page_number > 1:
            params['page'] = page_number - 1

        response = requests.get(url, params, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        soup_vacancies = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})

        for soup_vacancy in soup_vacancies:
            soup_title = soup_vacancy.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})
            soup_compensation = soup_vacancy.find('span', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
            compensation_min, compensation_max, compensation_currency = parse_compensation(soup_compensation)
            link = soup_title['href'].split('?')[0]
            soup_employer = soup_vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
            employer_name = soup_employer.text.replace('\xa0', ' ')
            soup_address = soup_vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
            address = soup_address.text.replace('\xa0', ' ')

            vacancies.append({
                'title': soup_title.text,
                'compensation_min': compensation_min,
                'compensation_max': compensation_max,
                'compensation_currency': compensation_currency,
                'link': link,
                'site': 'hh.ru',
                'employer_name': employer_name,
                'address': address
            })

        is_last_page = soup.find('a', {'data-qa': 'pager-next'}) is None
        if is_last_page:
            print(f'The vacancies were parsed from {page_number} pages.')
            break
        page_number += 1
        if page_number > page_count:
            print(f'The vacancies were parsed')
            break

    return vacancies


def parse_compensation(soup_compensation: element.Tag) -> (str, str, str):
    if soup_compensation is None:
        return None, None, None

    compensation = soup_compensation.text.replace('\u202f', '')
    m = re.search(r'(?P<min>\d+) ??? (?P<max>\d+) (?P<currency>\w+\.?)', compensation)
    if m is not None:
        return float(m.group('min')), float(m.group('max')), m.group('currency')

    m = re.search(r'???? (?P<min>\d+) (?P<currency>\w+\.?)', compensation)
    if m is not None:
        return float(m.group('min')), None, m.group('currency')

    # '???? 4000 EUR'
    m = re.search(r'???? (?P<max>\d+) (?P<currency>\w+\.?)', compensation)
    if m is not None:
        return None, float(m.group('max')), m.group('currency')

    raise ValueError('Argument compensation does not match any pattern. Define a new pattern and parsing rule to avoid this exception.')
