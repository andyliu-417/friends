# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TranscriptItem(scrapy.Item):
    # define the fields for your item here like:
    season = scrapy.Field()
    episode = scrapy.Field()
    who = scrapy.Field()
    content = scrapy.Field()

