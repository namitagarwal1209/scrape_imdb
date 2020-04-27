# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3

class CelebPipeline(object):


    def __init__(self):
        self.create_connction()
        self.create_table()

    def create_connction(self):
        self.conn = sqlite3.connect('celeb_db.db')
        self.curr = self.conn.cursor()


    def create_table(self):

        self.curr.execute("""DROP TABLE IF EXISTS celeb_table""")

        self.curr.execute("""create table celeb_table(
                                                        name text,
                                                        image text,
                                                        info text
                                                        )
                        """)


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into celeb_table values (?,?,?)""",
                          (item['name'][0],
                           item['image'][0],
                           item['info']
                           ))
        self.conn.commit()

