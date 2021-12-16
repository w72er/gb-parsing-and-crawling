from pprint import pprint

import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from avitoparser.items import LeroymerlinruItem


class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']
    # https://leroymerlin.ru/catalogue/garazhnye-vorota-i-rolstavni/

    def __init__(self, catalogue: str, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{catalogue}/']

    def parse(self, response: HtmlResponse, **kwargs):
        links = response.xpath('//a[@data-qa="product-image"]')
        for link in links:
            yield response.follow(link, callback=self.parse_product)
            print(link)

    @staticmethod
    def parse_product(response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinruItem(), response=response)
        loader.add_xpath('name', '//h1[@itemprop="name"]/text()')  # название
        loader.add_xpath('photos', '//source[contains(@srcset, "w_2000")]/@data-origin')  # все фото
        loader.add_value('url', response.url)  # ссылка
        loader.add_xpath('price', '//span[@slot="price"]/text()')  # цена
        yield loader.load_item()
