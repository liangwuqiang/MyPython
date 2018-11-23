# -*- coding: utf-8 -*-
import scrapy
from magnet.items import MagnetItem
import re
# from urllib.request import quote
from urllib.parse import quote
import json


class BturlSpider(scrapy.Spider):
    name = 'bturl'
    # allowed_domains = ['bturl.cc']
    # start_urls = ['https://www.bturl.cc/']
    # start_urls = [
    #               'file:///home/ubuntu/Documents/bturl1.html',
    #               'file:///home/ubuntu/Documents/bturl2.html',
    #               'file:///home/ubuntu/Documents/bturl3.html',
    #               'file:///home/ubuntu/Documents/bturltext.html',
    #               ]
    with open('bturl.txt', 'w') as f:
        f.write('')

    # """
        @staticmethod
        def get_url(keyword, sort, page):
            base_url = 'https://www.bturl.cc'  # bt磁力链
            sortby = 'ctime'
            if sort in '创建日期':
                sortby = 'ctime'
            elif sort in '文件大小':
                sortby = 'length'
            elif sort in '下载热度':
                sortby = 'click'
            return base_url + '/search/' + keyword.replace(' ', '%20') + '_' + sortby + '_' + str(page) + '.html'
    
        def start_requests(self):
            try:
                keyword = 'mkv'  # 搜索关键字
                sort = '创建日期'  # 排序
                start_page = 1  # 起始页数
                total_page = 3  # 爬取的页数
                for page in range(total_page):
                    url = self.get_url(keyword, sort, start_page + page)
                    print('url', url)
                    req = scrapy.Request(url)
                    # print(req)
                    yield req
            except Exception as e:
                print(e)
    # """

    def parse(self, response):
        try:
            hrefs = response.xpath('//ul/li/h3/a/@href').extract()
            for href in hrefs:
                href = 'https://www.bturl.cc' + href

                print('href', href)
                yield scrapy.Request(href, callback=self.parse_detail)
                # break
        except Exception as e:
            print(e)
        pass

    def parse_detail(self, response):
        item = MagnetItem()
        try:
            filename = response.xpath('//h1[@class="T1"]/text()')[0].extract()
            item['filename'] = filename
            detail = response.xpath('//dl[@class="BotInfo"]/p/text()')
            length = detail[0].extract()[6:]
            item['length'] = length
            ctime = detail[2].extract()[6:]
            item['ctime'] = ctime
            click = detail[3].extract()[6:]
            item['click'] = click
            link = response.xpath('//dl[@class="BotInfo"]/p/a/@href')[0].extract()
            item['link'] = link
            # yield item
            # 处理翻译
            str = re.findall('(.*?)\d', filename)[0]
            message = ' '.join(str.split('.')).lower()
            print(message)
            if str.endswith(' s'):
                message = message[:-2]
            item['baidu'] = message
            api = 'http://fanyi.youdao.com/openapi.do' \
                  '?keyfrom=wufeifei&key=716426270&type=data&doctype=json&version=1.1&q='
            api = api + quote(message)  # quote的作用是屏蔽特殊的字符  urllib.parse.quote(text)
            print(api)
            yield scrapy.Request(url=api, meta={'item': item}, callback=self.parse_fanyi)  #
        except Exception as e:
            print(e)
        # pass

    @staticmethod
    def parse_fanyi(response):
        item = response.meta['item']
        try:
            content = json.loads(response.text)
            fanyi = content["translation"][0]
            item['fanyi'] = fanyi[0:20]
            yield item
        except Exception as e:
            print('出错: ', e)
        pass
