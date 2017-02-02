#!/usr/bin/python
#-*- coding: utf-8 -*-

import scrapy
import sys
from facebook_scrapy.items import FacebookScrapyItem

class FacebookSpider(scrapy.Spider):
    name = 'facebook_scrapy'
    allowed_domains = ["m.facebook.com"]
    start_urls = ["https://m.facebook.com/chow.chu.92",
                  "https://m.facebook.com/hokchi.tong"]
    base_url = "https://m.facebook.com"

    def start_requests(self):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        return [scrapy.Request('https://m.facebook.com/login.php', meta={'cookiejar': 1}, callback=self.post_login)]

    def post_login(self, response):
        print 'Preparing login'
        lsd = scrapy.Selector(response).xpath('//input[@name="lsd"]/@value').extract_first()
        m_ts = scrapy.Selector(response).xpath('//input[@name="m_ts"]/@value').extract_first()
        li = scrapy.Selector(response).xpath('//input[@name="li"]/@value').extract_first()
        return [scrapy.FormRequest.from_response(
            response,
            meta={'cookiejar': response.meta['cookiejar']},
            formdata={
                'lsd': lsd,
                'm_ts': m_ts,
                'li': li,
                'email': 'your email address',
                'pass': 'your password'
            },
            callback=self.after_login
        )]

    def after_login(self, response):
        for url in self.start_urls:
            # print url
            yield scrapy.Request(url, meta={'cookiejar': response.meta['cookiejar']}, callback=self.parse_basic_info)
        return

    def parse_basic_info(self, response):
        item = FacebookScrapyItem()
        item['name'] = ''.join(scrapy.Selector(response).xpath('//title/text()').extract())
        item['sex'] = ''.join(scrapy.Selector(response).xpath('//*[@id="basic-info"]/div/div[2]/div/table/tr/td[2]/div/text()').extract())
        item['education'] = ''.join(scrapy.Selector(response).xpath('//*[@id="education"]/div/div[2]/div/div/div/div/div/span/a/text()').extract())
        item['quote'] = ''.join(scrapy.Selector(response).xpath('//*[@id="quote"]/div/div[2]/div/text()').extract())
        item['living'] = ''.join(scrapy.Selector(response).xpath('//*[@id="living"]/div/div[2]/div/div/table/tr/td[2]/div/a/text()').extract())
        yield item
        return
