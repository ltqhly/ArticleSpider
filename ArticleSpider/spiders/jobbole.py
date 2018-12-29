# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
# from urllib import parse  # python2中: import urlparse
import urlparse
from scrapy.loader import ItemLoader
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
import datetime


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):

        post_nodes = response.css("#archive div div.post-thumb a")
        # post_urls = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a/@href').extract()

        for post_node in post_nodes:
            print(post_node)
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")

            yield Request(url=urlparse.urljoin(response.url, post_url),
                          meta={"front_image_url": image_url, "page_url": response.url},
                          callback=self.parse_detail)
        # 提取下一页并交给scrapy进行下载
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=urlparse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        # re_selector = response.xpath('//*[@id="post-113771"]/div[1]/h1/text()')

        # article_item = JobBoleArticleItem()
        #
        # front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        # page_url = response.meta.get("page_url", "")  # 文章所在页面的url
        #
        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        #
        # create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace("·",
        #                                                                                                             "").strip()
        #
        # praise_nums = response.xpath(
        #     '//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract()[
        #     0].strip()
        # fav_nums = response.xpath(
        #     '//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()').extract()[0]
        #
        # match_re = re.match(".*?(\d+).*", fav_nums)
        # if match_re:
        #     fav_nums = match_re.group(1)
        # else:
        #     fav_nums = 0
        #
        # comment_nums = response.xpath('//a[@href="#article-comment"]/span/text()').extract()[0]
        # if match_re:
        #     comment_nums = match_re.group(1)
        # else:
        #     comment_nums = 0
        #
        # content = response.xpath("//div[@class='entry']/text()").extract()[0]
        #
        # tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        # try:
        #     create_date = datetime.datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.datetime.now().date()
        #
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["tags"] = tags
        # article_item["content"] = content
        # article_item["page_url"] = page_url

        # 通过Item Loader加载item
        front_image_url = response.meta.get("front_image_url", "")  # 文章封面图
        page_url = response.meta.get("page_url", "")  # 文章所在页面的url

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_css()
        # item_loader.add_value()
        item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_xpath("create_date", '//p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_value("page_url", "-")
        item_loader.add_xpath("comment_nums", '//a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath("praise_nums",
                              '//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()')
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_xpath("tags", "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        item_loader.add_xpath("content", '//div[@class="entry"]/text()')
        article_item = item_loader.load_item()

        yield article_item
