import scrapy
from scrawl.items import ScrawlItem


class TongchengSpider(scrapy.Spider):
    name = 'tongcheng'
    # 多页下载调整allowed_domains的范围
    allowed_domains = ['category.dangdang.com']
    start_urls = [
        'http://category.dangdang.com/cp01.01.07.00.00.00.html']
    # http://category.dangdang.com/pg2-cp01.01.07.00.00.00.html
    # http://category.dangdang.com/pg3-cp01.01.07.00.00.00.html
    base_url = 'http://category.dangdang.com/pg'
    page = 1

    # 地址以html结尾时在地址的末尾不需要加上/
    def parse(self, response):
        # 字符串数据
        # content = response.text
        # 二进制数据
        # content = response.body
        # print("=====================")
        # print(content)
        li_list = response.xpath('/html/body/div[2]/div/div[3]/div[1]/div[1]/div[2]/div/ul/li')
        # extract() 提取seletor对象的data属性值，存在一个list里。
        # extract_first()  返回的是一个string，提取seletor列表的第一个值。
        # 此时xpath路径应为具体路径，不能是//路径否则在全局搜索data属性值
        print("=====================")
        for span in li_list:
            # 所有seletor对象可再次调用xpath方法
            picture = span.xpath('./a/img/@data-original').extract_first()
            if picture:
                picture = picture
            else:
                picture = span.xpath('./a/img/@src').extract_first()
            name = span.xpath('./a/img/@alt').extract_first()
            price = span.xpath('./p[3]/span[1]/text()').extract_first()
            book = ScrawlItem(picture=picture, name=name, price=price)
            # 每获取一个book对象就将book对象传递给pipelines
            yield book

        if self.page < 4:
            self.page = self.page + 1
            url = self.base_url + str(self.page) + '-cp01.01.07.00.00.00.html'
            # scrapy.Request就是scrapy的get请求
            # url就是请求地址，注意URL需要在可以访问的域名之内
            # callback是要执行的函数
            # 这里可以另写一种方法对网页进行解析，此时callback = self.其他的方法，
            # 再去写方法，这样就能对其调用
            yield scrapy.Request(url=url,callback=self.parse)
            # yield中存在一个meta属性，当存在两个方法时可将上一个方法中的值用meta接收转为字典类型，再传递给下一个方法
            # 传递：yield scrapy.Request(url=url,callback=self.parse,meta{'name':name})
            # 接收：def sec_parse(self,response):
            #          name = response.meta['name']
            # 这样就能在一个方法中将所有对象传递给管道