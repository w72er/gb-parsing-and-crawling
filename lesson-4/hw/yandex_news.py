# Написать приложение, которое собирает основные новости с сайта на выбор:
# * news.mail.ru,
# * lenta.ru,
# * yandex-новости. <-- выбираю яндекс новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# * название источника;
# * наименование новости;
# * ссылку на новость;
# * дата публикации.
import requests
from lxml import html
import re
from datetime import date, timedelta


# <a href="https://yandex.ru/news/region/novosibirsk" target="_self" rel="noopener" data-log-id="u-1638505408000-ca13eb-37">Новосибирск</a>
# <a href="https://yandex.ru/news/rubric/politics" target="_self" rel="noopener" data-log-id="u-1638505408000-ca13eb-87">Политика</a>
# <a href="https://yandex.ru/news/rubric/society" target="_self" rel="noopener" data-log-id="u-1638505408000-ca13eb-127">Общество</a>
# я хочу выбрать категорию, в которой выбрать новости.

def get_yandex_news_html():
    url = 'https://yandex.ru/news/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}
    response = requests.get(url, headers=headers)
    return response.text if response.status_code == 200 else None


def get_main_news_block(html_page):
    dom = html.fromstring(html_page)
    news_block = dom.xpath('//div[contains(@class, "news-app__top")]')
    return news_block[0]


def get_date(time):
    m = re.search(r'^\d{2}:\d{2}$', time)
    if m is not None:
        return date.today()

    m = re.search(r'^вчера в \d{2}:\d{2}$', time)
    if m is not None:
        return date.today() - timedelta(days=1)

    # 1 декабря в 15:54
    raise ValueError('Argument time does not match any pattern. Define a new pattern and parsing rule to avoid this exception.')


def encode(s):
    return s.replace(u'\xa0', ' ')


def get_news(news_block):
    source_titles = news_block.xpath('.//a[@class="mg-card__source-link"]/text()')
    titles = news_block.xpath('.//*[@class="mg-card__title"]/text()')
    links = news_block.xpath('.//a[@class="mg-card__link"]/@href')
    published_ats = news_block.xpath('.//span[@class="mg-card-source__time"]/text()')

    news = []
    for i in range(len(titles)):
        news.append({
            'source_title': encode(source_titles[i]),
            'title': encode(titles[i]),
            'link': encode(links[i]),
            'published_at': get_date(encode(published_ats[i]))
        })

    return news
