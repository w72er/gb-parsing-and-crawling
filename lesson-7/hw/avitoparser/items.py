# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy


def clear_avitoparser_price(value):
    value = value.replace('\xa0', '')
    try:
        return int(value)
    except:
        return value


def clear_leroymerlinru_price(value):
    value = value.replace(' ', '')
    try:
        return int(value)
    except ValueError:
        return value


class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_avitoparser_price))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_avitoparser_price))
    url = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()


class LeroymerlinruItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    url = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=MapCompose(clear_leroymerlinru_price))
