"""
 Ранер позволяет запускать скрапер в режиме отладки
"""
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
# from jobparser.spiders.superjob import SuperjobSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(HhruSpider)
    # process.crawl(SuperjobSpider)

    process.start()

