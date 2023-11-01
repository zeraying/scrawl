# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


# 使用管道，必须在setting中开启管道
class ScrawlPipeline:
    # 在爬虫文件开始之前就执行这个方法
    def open_spider(self, spider):
        self.a = open("book.json", "a", encoding="utf-8")

    # item是yield传递过来的book对象
    def process_item(self, item, spider):
        # 每传过来一个对象就打开一次文件，对文件操作太过频繁
        # with open("book.json","a",encoding="utf-8")as fp:
        #     # write方法必须写入字符串而不是对象，可以用字符串强转
        #     fp.write(str(item))
        print(item)
        self.a.write(str(item))
        return item

    # 在爬虫文件执行完后执行这个方法
    def close_spider(self, spider):
        self.a.close()


import urllib.request


# 开启多条管道
# 注意要在settings中开启此管道
class pipline2:
    def process_item(self, item, spider):
        picture = 'http:' + item.get('picture')
        name = './books/' + item.get('name') + '.jpg'
        urllib.request.urlretrieve(url=picture, filename=name)
        return item