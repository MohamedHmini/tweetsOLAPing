import scrapy
from .TweetsPoolItem import TweetsPoolItem



class archivedTweetsScrapper(scrapy.Spider):
    name = "test"
    start_urls = []
    def start_requests(self):
        yield scrapy.Request("https://archive.org/download/archiveteam-twitter-stream-2017-07/twitter-stream-2017-07-04.tar/", self.parse)
    
    def parse(self, response):
       self.logger.info(f"test %s " % response.css('div').getall())

        

        