import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class SuperjobruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = [
        'https://nsk.superjob.ru/vacancy/search/?keywords=developer'
    ]

    def parse(self, response: HtmlResponse, **kwargs):
        """ Откроем следующую страницу и распарсим текущую. """

        next_href_xpath = '//a[@rel="next"]//*[text()="Дальше"]//ancestor::a/@href'
        next_href = response.xpath(next_href_xpath).get()
        if next_href:
            yield response.follow(next_href, callback=self.parse)

        href = "/vakansii/chat-operator-1s-40582454.html?search_id=0e9397e8-5b49-11ec-bb3f-ff1077e66520&vacancyShouldHighlight=true"

        vacancy_links = response.xpath(
            '//div[@class="f-test-search-result-item"]//a[contains(@href, "vakansii") and not(@rel="nofollow")]/@href').getall()

        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancy)
        pass

    @staticmethod
    def parse_vacancy(response: HtmlResponse, **kwargs):
        name = response.xpath('//div[contains(@class, "f-test-address")]/../h1//text()').get()
        salary = response.xpath('//div[contains(@class, "f-test-address")]/../span//text()').getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
