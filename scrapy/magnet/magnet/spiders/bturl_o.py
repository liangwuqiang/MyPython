# -*- coding: utf-8 -*-

"""
功能：   爬去bt磁力链的磁力链接，以便可以通过网页html方式直接点击下载
"""

import scrapy
from magnet.items import MagnetItem
import re
# from urllib.request import quote
from urllib.parse import quote
import json


class BturlSpider(scrapy.Spider):
    name = 'bturl_o'
    # allowed_domains = ['bturl.cc']
    # start_urls = ['https://www.bturl.cc/']
    # start_urls = [
    #               'file:///home/ubuntu/Documents/bturl1.html',
    #               'file:///home/ubuntu/Documents/bturl2.html',
    #               'file:///home/ubuntu/Documents/bturl3.html',
    #               'file:///home/ubuntu/Documents/bturltext.html',
    #               ]
    # with open('bturl.txt', 'w') as f:
    #     f.write('')

    # """
    @staticmethod
    def get_url(keyword, sort, page):
        base_url = 'https://www.bturl.so'  # bt磁力链
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
            keyword = 'Starship Troopers'  # 搜索关键字
            sort = '文件大小'  # 排序
            start_page = 3  # 起始页数
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
                href = 'https://www.bturl.so' + href

                print('href', href)  # ========================
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
            print(link)
            yield item

        except Exception as e:
            print(e)
        # pass
"""
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
"""
