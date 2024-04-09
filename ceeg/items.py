# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CeegItem(scrapy.Item):

    # 入库时间
    ctime = scrapy.Field(serializer=str)
    # 网址
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 发布时间
    publishtime = scrapy.Field()

