# -*- coding: utf-8 -*-
import scrapy
from scrapies.items import TranscriptItem
import re
import os

class TranscriptSpider(scrapy.Spider):
    name = 'transcript'
    allowed_domains = ['livesinabox.com']
    start_urls = ["http://www.livesinabox.com/friends/scripts.shtml"]
    path = os.path.abspath(os.path.join(os.getcwd(), "../transcripts"))

    def start_requests(self):
        yield scrapy.Request("http://www.livesinabox.com/friends/scripts.shtml", self.parse_index)

    def filter_tags(self, htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile(
            '<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile(
            '<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        # blank_line = re.compile('\n+')
        # s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    def replaceCharEntity(self, htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def parse_index(self, response):
        episodes = response.css('ul li')
        for episode in episodes:
            href = episode.css('a::attr(href)').extract_first()
            episode_url = response.urljoin(href)
            # print(episode_url)
            yield scrapy.Request(url=episode_url, callback=self.parse_transcript)

    def parse_transcript(self, response):
        result = re.findall(r"/(\d+)", response.url)[0]
        season = int(int(result)/100)
        episode = int(result) - season*100
        transcript_name = str(season) + '-' + str(episode) + ".txt"
        transcript_path = os.path.join(self.path, transcript_name)

        content = self.filter_tags(response.text)
        with open(transcript_path, 'a') as transcript:
            transcript.write(content + '\n')
        print("文件名为: ", transcript.name)



    # item = ScrapiesItem()
    # item['season'] = "saasdf"
    # item['episode'] = 'sadf'
    # item['who'] = 'asdf'
    # item['content'] = 'asdfdsf'
    # yield item
