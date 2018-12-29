# -*- coding: utf-8 -*-
import scrapy


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        # post_urls = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/@href').extract()

        channel = response.xpath('//div[@class="navlst2"]/ul/li/a')

        pass
