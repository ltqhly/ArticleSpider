# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime
from scrapy.loader import ItemLoader
import re
import requests
import json


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()
    return create_date


def get_num(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = match_re.group(1)
    else:
        nums = 0
    return int(nums)


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


"""
-------------------------------------------------
scrapy引入processor: from scrapy.loader.processors import MapCompose, TakeFirst, Join
关于集中声明 input and output processors方式的优先级排序如下：
1.在Item Loader 中声明的 field-specific 属性: field_in and field_out (most precedence)
2.Item中的字段元数据(input_processor and output_processor key)
3.Item Loader 默认处理器: ItemLoader.default_input_processor() and ItemLoader.default_output_processor() (least precedence)
-------------------------------------------------
"""


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    content = scrapy.Field()
    page_url = scrapy.Field()
    pass


"""
-------------------------------------------------
丁香园
-------------------------------------------------
"""


class dxytagItem(scrapy.Item):
    channel = scrapy.Field()
    tag = scrapy.Field()
    pass


class DxyItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def networkGetJson(value):
    request = requests.get(value).text
    data = json.loads(request)
    num = data['message']['total']
    return num


def remove_html(html):
    reg = re.compile('<[^>]*>')
    text = reg.sub('', html)
    return text


class DxyItem(scrapy.Item):
    title = scrapy.Field()  # 文章标题
    create_date = scrapy.Field(
        input_processor=MapCompose(date_convert)
    )  # 文章创建时间
    author = scrapy.Field()  # 作者
    source = scrapy.Field()  # 文章来源
    url = scrapy.Field()  # 文章url
    # page_url = scrapy.Field()  # 文章所在页面url
    channel = scrapy.Field()  # 文章所在频道 eg: 心血管
    tag = scrapy.Field()  # 文章标签 eg: 最新资讯
    praise_nums = scrapy.Field(
        input_processor=MapCompose(networkGetJson)
    )  # 点赞数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(networkGetJson)
    )  # 收藏数
    content_html = scrapy.Field()  # 文章内容html
    content = scrapy.Field(
        input_processor=MapCompose(remove_html)
    )  # 文章内容
    pass
