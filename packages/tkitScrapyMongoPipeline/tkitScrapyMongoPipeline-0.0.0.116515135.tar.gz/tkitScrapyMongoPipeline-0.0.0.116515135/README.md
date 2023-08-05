# tkitScrapyMongoPipeline
# MongoPipeline

https://docs.scrapy.org/en/latest/topics/item-pipeline.html


数据存储到mongodb




```commandline



# settings
# 1、设置MongoDB 的数据库地址
MONGO_URI = "mongodb://192.168.123.117:27017/"
MONGO_DATABASE="test"
# # 2、启用中间件MongoPipeline
ITEM_PIPELINES = {
   # 'base.pipelines.DuplicatesPipeline': 100,
   'base.pipelines.MongoPipeline': 100,
}








# item 字段示例
 item={
#设置强制去重复字段
"dup_id":url,
"title": title, "url": url, "content": text, "site": "playbarkrun.com", "content_type": "content",
# 设置表名
"collection_name":"test11"
}



```






详细参考

> dev.md


