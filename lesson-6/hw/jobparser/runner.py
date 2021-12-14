"""
 Ранер позволяет запускать скрапер в режиме отладки
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.superjobru import SuperjobruSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(HhruSpider)
    process.crawl(SuperjobruSpider)

    process.start()

