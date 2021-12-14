import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        # 'https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&ored_clusters=true&enable_snippets=true&salary=&text=Scala&from=suggest_post',
        'https://novosibirsk.hh.ru/search/vacancy?clusters=true&area=4&ored_clusters=true&enable_snippets=true&salary=&text=%D0%98%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80+%D0%BF%D0%BE+%D0%B0%D0%B2%D1%82%D0%BE%D1%82%D0%B5%D1%81%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8E%2FQA+Automation'
    ]

    def parse(self, response: HtmlResponse, **kwargs):
        next_page = response.xpath('//a[@data-qa="pager-next"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//a[@data-qa="vacancy-serp__vacancy-title"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    @staticmethod
    def vacancy_parse(response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath("//div[@class='vacancy-salary']//text()").getall()
        link = response.url
        item = JobparserItem(name=name, salary=salary, link=link)
        yield item
