from scrapy.crawler import CrawlerProcess
from instaparser.spiders.insta_hw import InstaHwSpider

from scrapy.settings import Settings
from instaparser import settings


if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaHwSpider, usernames=['pakjimin47', 'vasilisa_vasyx.x.x'])
    process.start()
