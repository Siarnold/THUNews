# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThuSpiderItem(scrapy.Item):
    sqlite_keys = ["news_id"]
    news_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    content = scrapy.Field()
