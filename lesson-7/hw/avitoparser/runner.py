import sys
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from avitoparser.spiders.avito import AvitoSpider
from avitoparser.spiders.leroymerlinru import LeroymerlinruSpider
from avitoparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    # search = input('')
    search = 'вафли+say+cheese'  # "квартиры"
    process.crawl(AvitoSpider, search=search)
    # 'okna-i-dveri' or 'garazhnye-vorota-i-rolstavni'
    process.crawl(LeroymerlinruSpider, catalogue='garazhnye-vorota-i-rolstavni')
    process.start()
