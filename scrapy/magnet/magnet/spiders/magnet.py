"""
功能：爬去网页中的磁力链接，以便可以通过网页html方式直接点击下载
"""

import scrapy
from magnet.items import MagnetItem
import re
from urllib.parse import quote
import json


class MagnetSpider(scrapy.Spider):
    # 基本的参数设置
    name = 'magnet'  # 蜘蛛的名字

    web = 'ciliba'  # bturl、ciliba、cilimao
    keyword = '2160p'  # 搜索关键字
    sort = '大小'  # 排序 （时间、热度、大小）
    start_page = 2  # 起始页数
    total_page = 1  # 爬取的页数
    # 不需要设置的参数
    base_url = ''
    main_xpath = ''

    def get_url(self, page):
        sort_dict = {
            'bturl': {'时间': 'ctime', '大小': 'length', '热度': 'click'},
            'ciliba': {'时间': 'time', '大小': 'size', '热度': 'hits'},
            'cilimao': {'时间': 'created_time', '大小': 'content_size', '热度': 'download_count'},
        }
        sort = sort_dict[self.web][self.sort]
        if self.web == 'bturl':  # bt磁力链
            self.main_xpath = '//ul/li/h3/a/@href'
            self.base_url = 'https://www.bturl.so'
            # https://www.bturl.so/search/我不是药神_ctime_1.html
            return 'https://www.bturl.so/search/'\
                   + quote(self.keyword) + '_' + sort + '_' + str(page) + '.html'
        elif self.web == 'ciliba':  # 磁力吧
            self.main_xpath = '//div[@class="item-title"]/h3/a/@href'
            # https://www.ciliba.biz/s/摩天营救_time_2.html
            return 'https://www.ciliba.biz/s/'\
                   + quote(self.keyword) + '_' + sort + '_' + str(page) + '.html'
        elif self.web == 'cilimao':  # 磁力猫
            # //*[@id="Search__content_left___2MajJ"]/div[9]/div[1]/a
            # //*[@id="Search__content_left___2MajJ"]/div[9]/div[2]/a
            self.main_xpath = '//*[@id="Search__content_left___2MajJ"]/div[9]/div/a/@href'
            # https://www.cilimao.cc/search?word=如懿传&sortProperties=download_count&page=3
            return 'https://www.cilimao.cc/search?word='\
                   + quote(self.keyword) + '&sortProperties=' + sort + '&page=' + str(page) + '.html'

    def start_requests(self):
        try:
            for page in range(self.total_page):
                url = self.get_url(self.start_page + page)
                print('url', url)
                yield scrapy.Request(url)
        except Exception as e:
            print('====start_requests====', e)

    def parse(self, response):
        try:
            hrefs = response.xpath(self.main_xpath).extract()
            for href in hrefs:
                href = self.base_url + href
                print('====解析出来的链接====', href)
                yield scrapy.Request(href, callback=self.parse_detail)
                # break
        except Exception as e:
            print(e)
        pass

    def parse_detail(self, response):
        item = MagnetItem()
        try:
            if self.web == 'bturl':
                item['filename'] = response.xpath('//h1[@class="T1"]/text()')[0].extract()
                detail = response.xpath('//dl[@class="BotInfo"]/p/text()')
                item['length'] = detail[0].extract()[6:]
                item['ctime'] = detail[2].extract()[6:]
                item['click'] = detail[3].extract()[6:]
                item['link'] = response.xpath('//dl[@class="BotInfo"]/p/a/@href')[0].extract()
            if self.web == 'ciliba':
                item['filename'] = response.xpath('//h1[@class="res-title"]/text()')[0].extract()
                detail = response.xpath('//div[@class="fileDetail"]/p/text()')
                item['length'] = detail[0].extract()[6:]
                item['ctime'] = detail[1].extract()[6:]
                item['click'] = response.xpath('//*[@id="hits_num"]/text()')[0].extract()  # 动态网页，取不到数值
                item['link'] = response.xpath('//*[@id="down-link"]/@href')[0].extract()
            if self.web == 'cilimao':
                item['filename'] = response.xpath('//h1[@class="res-title"]/text()')[0].extract()
                item['length'] = response.xpath('//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[3]/text()')[0].extract()
                item['ctime'] = response.xpath('//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[4]/text()')[0].extract()
                item['click'] = '未提供'
                item['link'] = response.xpath('//*[@id="Information__container___2meHB"]/div[2]/div[2]/a/@href')[0].extract()

            # 处理翻译
            message = re.findall('(.*?)\d', item['filename'])[0]
            message = ' '.join(message.split('.')).lower()
            # print(message)
            if message.endswith(' s'):
                message = message[:-2]
            item['baidu'] = message
            api = 'http://fanyi.youdao.com/openapi.do' \
                  '?keyfrom=wufeifei&key=716426270&type=data&doctype=json&version=1.1&q='
            api = api + quote(message)  # quote的作用是屏蔽特殊的字符  urllib.parse.quote(text)
            # print(api)
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
            item['fanyi'] = fanyi[:30]
            yield item
        except Exception as e:
            print('翻译出错: ', e)
        pass
