import scrapy
import os
from .TweetsPoolItem import TweetsPoolItem


def parse_source_file():
    srs = []
    with open(os.path.abspath("../../tweetsPOOLs.csv"), 'r') as f:
        srs = f.read().split('\n')
    c = srs.copy()
    srs = []
    for src in c:
        srs.append(src.split(','))
    return srs


class archivedTweetsScrapper(scrapy.Spider):
    name = "tweets"
    start_urls = []

    def start_requests(self):
        root_count = 1
        for src in parse_source_file():
            yield scrapy.Request(src[1], self.parse, meta = {'rootCount' : root_count})
            root_count += 1
    
    def parse(self, response):
        sub_count = 1
        for href in response.xpath('//a[contains(text(),"View Contents")]/@href').getall():
            yield scrapy.Request(
                f"%s/%s" % (response.url, href), 
                self.parse_substream, 
                meta= {'rootCount' : response.meta.get('rootCount'), 'subCount' : sub_count}
            )
            sub_count += 1

    def parse_substream(self, response):
        for href in response.xpath('//a[contains(text(),".json.bz2")]/@href').getall():
            yield TweetsPoolItem(
                grain_stream = href, 
                sub_stream = response.meta.get('subCount'), 
                root_stream = response.meta.get('rootCount')
            )



        

        