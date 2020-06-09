import scrapy






class TweetsPoolItem(scrapy.Item):
    grain_stream = scrapy.Field()
    sub_stream = scrapy.Field()
    root_stream = scrapy.Field()
