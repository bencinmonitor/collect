# -*- coding: utf-8 -*-
import scrapy


class Station(scrapy.Item):
    scraped_at = scrapy.Field()
    scraped_url = scrapy.Field()
    images = scrapy.Field()
    image_urls = scrapy.Field()
    name = scrapy.Field()
    address = scrapy.Field()
    lon = scrapy.Field()
    lat = scrapy.Field()
    xid = scrapy.Field()  # ID on page
    xcode = scrapy.Field()  # Internal ID if possible
