from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from instaparser.spiders.insta_hw import InstaHwSpider
from instaparser.spiders.instagram import InstaSpider


if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl(InstaSpider)
    process.crawl(InstaHwSpider, usernames=['pakjimin47', 'vasilisa_vasyx.x.x', 'sharapgplieva24'])
    process.start()
