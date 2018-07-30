# -*- coding: utf-8 -*-
import scrapy
from scrapies.items import ScrapiesItem
import re


class TranscriptSpider(scrapy.Spider):
    name = 'transcript'
    allowed_domains = ['livesinabox.com']
    start_urls = ["http://www.livesinabox.com/friends/scripts.shtml"]

    def start_requests(self):
        yield scrapy.Request("http://www.livesinabox.com/friends/scripts.shtml", self.parse_index)

    def parse_index(self, response):
        episodes = response.css('ul li')
        for episode in episodes:
            href = episode.css('a::attr(href)').extract_first()
            episode_url = response.urljoin(href)
            # print(episode_url)
            yield scrapy.Request(url=episode_url, callback=self.parse_transcript)

    def parse_transcript(self, response):
        result = re.findall("/(\d+)", response.url)[0]
        season = int(int(result)/100)
        episode = int(result) - season*100

        if (season == 9 and episode == 15):
            pass
        else:
            pass
            



        # item = ScrapiesItem()
        # item['season'] = "saasdf"
        # item['episode'] = 'sadf'
        # item['who'] = 'asdf'
        # item['content'] = 'asdfdsf'
        # yield item
