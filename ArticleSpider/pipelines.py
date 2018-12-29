# -*- coding: utf-8 -*-

import codecs
import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
# import MySQLdb
# import MySQLdb.cursors
from w3lib.html import remove_tags
import psycopg2


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        # print("sddsadf")
        print item
        return item


# class MysqlPipeline(object):
#     # 采用同步的机制写入mysql
#     def __init__(self):
#         self.conn = MySQLdb.connect('localhost', 'root', 'hanbaobao0315', 'ScrapyDB', charset="utf8", use_unicode=True)
#         self.cursor = self.conn.cursor()
#
#     def process_item(self, item, spider):
#         insert_sql = """
#             INSERT INTO articale(title,create_date,url,url_object_id,front_image_url,front_image_path,page_url,comment_nums,fav_nums,praise_nums,tags,content)
#             VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)
#         """
#
#         self.cursor.execute(insert_sql, (
#             item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
#             item["front_image_path"], item["page_url"], item["comment_nums"], item["fav_nums"], item["praise_nums"],
#             item["tags"], item["content"]))
#         self.conn.commit()

class dxyDBPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        # self.conn = MySQLdb.connect('localhost', 'root', '', 'ScrapyDB', charset="utf8", use_unicode=True)
        self.conn = psycopg2.connect(database="Article", user="liutanqi", password="", host="127.0.0.1", port="5432")
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        print "插入", item
        insert_sql = """
            INSERT INTO article(
            title,
            create_date,
            author,
            source,
            url,
            channel,
            tag,
            praise_nums,
            fav_nums,
            content_html,
            content
            )
            VALUES (
             %s, 
             %s, 
             %s,
             %s, 
             %s, 
             %s, 
             %s,
             %s, 
             %s, 
             %s, 
             %s
             )
        """

        self.cursor.execute(insert_sql, (
            item["title"],
            item["create_date"],
            item["author"],
            item["source"],
            item["url"],
            item["channel"],
            item["tag"],
            item["praise_nums"],
            item["fav_nums"],
            item["content_html"],
            item["content"]))
        self.conn.commit()


class MysqlTwistedPipline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
            INSERT INTO articale(title,create_date,url,url_object_id,front_image_url,front_image_path,page_url,comment_nums,fav_nums,praise_nums,tags,content)
            VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)
        """

        cursor.execute(insert_sql, (
            item["title"], item["create_date"], item["url"], item["url_object_id"], item["front_image_url"],
            item["front_image_path"], item["page_url"], item["comment_nums"], item["fav_nums"], item["praise_nums"],
            item["tags"], item["content"]))


class JsonWithEncodingPipline(object):
    def __init__(self):
        self.file = codecs.open('article.json', 'w', encoding="utf-8")

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)

        return item

    def spider_closed(self, spider):
        self.file.close()


class ArticleImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
                item["front_image_path"] = image_file_path
                return item

        pass
