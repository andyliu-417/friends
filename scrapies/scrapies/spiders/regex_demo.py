# -*- coding: utf-8 -*-
import scrapy
import re


class RegexDemoSpider(scrapy.Spider):
    name = 'regexdemo'
    allowed_domains = ['livesinabox.com']
    start_urls = ["http://www.livesinabox.com/friends/scripts.shtml"]

    def start_requests(self):
        yield scrapy.Request("http://www.livesinabox.com/friends/season1/112towdl.htm", self.parse_index)

    def clean_response(self, response):
        remove_tags = ["<b>", "</b>", "<strong>",
                       "</strong>", "<font>", "</font>"]
        for tag in remove_tags:
            response = response.replace(tag, '')
        return response

    def parse_index(self, response):
        # transcript = self.clean_response(response.text.strip())
        # whos = response.css('p b::text').extract()
        # ' '.join(t.strip() for t in response.css('p ::text').extract()).strip()
        # ps = response.css('p ::text').extract()
        # for p in ps:

        #     print(p.strip().rstrip(':'))
        ret = ' '.join(t.strip() for t in response.css('p ::text').extract()).strip()
        print(ret)
        return
        re_line = r"<p>([\s\S]*)</p>"
        lines = re.findall('/[-~]/', transcript)
        for line in lines:
            print(line)
            who = line[0].strip()
            content = line[1].strip()
            # print(who)
            # print(content)
        print(len(lines))
        
