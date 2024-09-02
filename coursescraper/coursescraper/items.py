# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CourseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    learning_outcomes = scrapy.Field()
    prerequisites = scrapy.Field()
    
