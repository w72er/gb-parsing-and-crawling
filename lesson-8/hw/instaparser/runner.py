from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from instaparser.spiders.insta_hw import InstaHwSpider
from instaparser.spiders.instagram import InstaSpider

from scrapy.settings import Settings
from instaparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # process = CrawlerProcess(get_project_settings())
    # process.crawl(InstaSpider)
    # process.crawl(InstaHwSpider, usernames=['pakjimin47', 'vasilisa_vasyx.x.x'])
    process.crawl(InstaHwSpider, usernames=['pakjimin47'])
    process.start()
