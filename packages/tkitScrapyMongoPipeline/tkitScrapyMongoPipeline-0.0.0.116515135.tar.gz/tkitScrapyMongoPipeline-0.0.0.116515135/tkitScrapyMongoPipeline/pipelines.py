# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface


from scrapy.exceptions import DropItem

import pymongo
from itemadapter import ItemAdapter

# class DuplicatesPipeline:
#     """
#     去重复
#     Scrapy使用Pipeline过滤重复数据
#     https://www.jianshu.com/p/7c1d20983540
#
#     id字段进行强制去重复
#
#
#     """
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     # def process_item(self, item, spider):
#     #     adapter = ItemAdapter(item)
#     #     if adapter['id'] in self.ids_seen:
#     #         raise DropItem(f"Duplicate item found: {item!r}")
#     #     else:
#     #         self.ids_seen.add(adapter['id'])
#     #         return item
#     def process_item(self, item, spider):
#         adapter = ItemAdapter(item)
#         if adapter['url'] in self.ids_seen:
#             raise DropItem(f"Duplicate item found: {item!r}")
#         else:
#             self.ids_seen.add(adapter['url'])
#             return item


"""
参考地址

https://docs.scrapy.org/en/latest/topics/item-pipeline.html

"""


class MongoPipeline:
    """
    数据存储到mongodb


    """

    collection_name = 'scrapy_items'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        yield {
        #设置强制去重复字段
        "dup_id":url,
        "title": title, "url": url, "content": text, "site": "playbarkrun.com", "content_type": "content",
        # 设置表名
        "collection_name":"test11"
        }


        :param item:
        :param spider:
        :return:
        """

        # adapter = ItemAdapter(item)
        # if adapter['url'] in self.ids_seen:
        #     raise DropItem(f"Duplicate item found: {item!r}")
        # else:
        #     self.ids_seen.add(adapter['url'])
        #     return item

        # 设置自动插入表
        # 可以通过返回数据item中item["collection_name"]设置
        if item.get("collection_name"):
            self.collection_name = item.get("collection_name")
            # 删除表字段
            # del item["collection_name"]

        if item.get("dup_id"):
            # 如果包含去重复字段则自动去重复
            # 字段查询重复
            adapter = ItemAdapter(item)
            if self.db[self.collection_name].find({'dup_id': adapter['dup_id']}):
                # if adapter['did'] in self.ids_seen:
                raise DropItem(f"Duplicate item found: {item!r}")
            else:
                pass

        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
