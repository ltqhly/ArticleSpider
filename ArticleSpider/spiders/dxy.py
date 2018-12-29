# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from ArticleSpider.items import dxytagItem, DxyItem, DxyItemLoader
import time
# from urllib import parse  # python2中: import urlparse
import urlparse
import requests
import json
from scrapy_redis.spiders import RedisSpider


class DxySpider(RedisSpider):
    name = 'dxy'
    # allowed_domains = ['www.dxy.cn']
    redis_key = 'dxy1:start_url'
    # start_urls = ['http://www.dxy.cn/']

    def parse(self, response):
        # time.sleep(2)
        channel_list = response.xpath('//div[@class="navlst2"]/ul/li/a')
        for channel in channel_list:
            # channelName = channel.css("::attr(text)").extract_first("")
            channelName = channel.xpath("text()").extract_first("")
            channelHref = channel.css("::attr(href)").extract_first("")
            meta = {"channelName": channelName,
                    "channelHref": channelHref}

            yield Request(url=channelHref, meta=meta, callback=self.parse_channel)

    def parse_channel(self, response):
        # time.sleep(2)
        channelName = response.meta.get("channelName", "")
        channelHref = response.meta.get("channelHref", "")
        tag_list = response.xpath('//ul[@class="dz"]/li/a')
        for tag in tag_list:
            # time.sleep(1)
            tagName = tag.xpath("text()").extract_first("")
            tagHref = tag.xpath("@href").extract_first("")
            if tagName not in [u'频道首页', u'丁香公开课']:
                meta = {"channelName": channelName,
                        "channelHref": channelHref,
                        "tagName": tagName,
                        "tagHref": tagHref}
                yield Request(url=tagHref, meta=meta, callback=self.parse_tag, dont_filter=True)
            # else:

    def parse_tag(self, response):
        # time.sleep(2)
        channelName = response.meta.get("channelName", "")
        channelHref = response.meta.get("channelHref", "")
        tagName = response.meta.get("tagName", "")
        tagHref = response.meta.get("tagHref", "")

        article_list = response.xpath('//div[@class="x_wrap1 fl"]/dl/dd/p[@class="title"]')
        for article in article_list:
            article_date = article.xpath("span/text()").extract_first("")
            article_url = article.xpath("a/@href").extract_first("")
            article_title = article.xpath("a/text()").extract_first("")
            meta = {"channelName": channelName,
                    "channelHref": channelHref,
                    "tagName": tagName,
                    "tagHref": tagHref,
                    "articleURL": article_url,
                    "articleTitle": article_title}
            posturl = urlparse.urljoin(response.url, article_url)
            time.sleep(2)
            yield Request(url=posturl, meta=meta, callback=self.parse_detail)
            # 提取下一页并交给scrapy进行下载
        next_url = response.xpath("//div[@class='el_page x_page1']/a").extract_first()
        if next_url:
            yield Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse_tag)

            # item = dxytagItem()
            # item["channel"] = channelName
            # item["tag"] = tagName
            # yield item

    def parse_detail(self, response):

        # time.sleep(5)
        article_title = response.meta.get("articleTitle", "")
        articleURL = response.meta.get("articleURL", "")
        channelName = response.meta.get("channelName", "")
        channelHref = response.meta.get("channelHref", "")
        tagName = response.meta.get("tagName", "")
        tagHref = response.meta.get("tagHref", "")

        # # all = response.xpath('//div[@id="j_article_desc"]')
        # article_source = response.xpath('//div[@class="x_box13"]/div[@class="sum"]/span[2]/a/text()').extract_first("")
        # article_author = response.xpath('//div[@class="x_box13"]/div[@class="sum"]/span[3]/text()').extract_first("")
        # # article_praise = response.xpath('//div[@id="art-like"]/a/span[@class="num"]').extract_first("")
        # # article_collect = response.xpath('//div[@id="art-favo"]/a/span[@class="num"]').extract_first("")
        # article_contentHtml = response.xpath('//div[@id="content"]').extract_first("")
        article_id = articleURL.split('/')[-1]
        collect_url = 'http://gi.dxy.cn/webservices/like-shareV2/likenum?id={article_id}&type=1&plat=9&ctype=1'.format(
            article_id=article_id)
        praise_url = 'http://gi.dxy.cn/webservices/like-shareV2/likenum?id={article_id}&type=1&plat=9&ctype=2'.format(
            article_id=article_id)
        # conllect_request = requests.get(collect_url).text
        # collect_data = json.loads(conllect_request)
        # article_collect = collect_data['message']['total']
        # praise_request = requests.get(praise_url).text
        # praise_data = json.loads(praise_request)
        # praise_collect = praise_data['message']['total']

        item_loader = DxyItemLoader(item=DxyItem(), response=response)
        item_loader.add_value("title", article_title)
        item_loader.add_value("url", articleURL)
        item_loader.add_xpath("source", '//div[@class="x_box13"]/div[@class="sum"]/span[2]/a/text()')
        item_loader.add_xpath("author", '//div[@class="x_box13"]/div[@class="sum"]/span[3]/text()')
        item_loader.add_xpath("content_html", '//div[@id="content"]')
        item_loader.add_xpath("content", '//div[@id="content"]')
        item_loader.add_value("praise_nums", praise_url)
        item_loader.add_value("fav_nums", collect_url)
        # item_loader.add_value("fav_nums", collect_url)
        item_loader.add_value("channel", channelName)
        item_loader.add_value("tag", tagName)
        item_loader.add_value("create_date", "")

        article_item = item_loader.load_item()
        yield article_item

        # print("dsfsdafsadfdsf")
    # title = scrapy.Field()
    # create_date = scrapy.Field()
    # author = scrapy.Field()
    # source = scrapy.Field()
    # url = scrapy.Field()
    # page_url = scrapy.Field()
    # channel = scrapy.Field()
    # tag = scrapy.Field()
    # praise_nums = scrapy.Field()
    # fav_nums = scrapy.Field()
    # content_html = scrapy.Field()
    # content = scrapy.Field()
