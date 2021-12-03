from pprint import pprint
from yandex_news import get_yandex_news_html, get_main_news_block, get_news
from gb_db_news import GbDbNews


if __name__ == '__main__':
    html_page = get_yandex_news_html()
    print(html_page[:100])
    xpath_main_news_block = get_main_news_block(html_page)
    news = get_news(xpath_main_news_block)
    # for new in news:
    #     pprint(new)

    with GbDbNews() as news_db:
        # news_db.news.delete_many({})
        news_db.create_indexes()
        news_db.add(news)
        for n in news_db.show():
            pprint(n)
