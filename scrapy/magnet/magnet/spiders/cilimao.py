"""
网页：磁力猫
功能：爬去网页中的磁力链接，以html方式显示
"""

import scrapy
from magnet.items import MagnetItem
import re
from urllib.parse import quote
import json


class MagnetSpider(scrapy.Spider):
    name = 'cilimao'  # 蜘蛛的名字
    keyword = '2160p'  # 搜索关键字
    sort = '大小'  # 排序 （时间、热度、大小）
    start_page = 2  # 起始页数
    total_page = 1  # 爬取的页数
    # 不需要设置的参数

    def get_url(self, page):
        sort_dict = {'时间': 'created_time', '大小': 'content_size', '热度': 'download_count'}
        sort = sort_dict[self.sort]
        # https://www.cilimao.cc/search?word=如懿传&sortProperties=download_count&page=3
        return 'https://www.cilimao.cc/search?word='\
               + quote(self.keyword) + '&sortProperties=' + sort + '&page=' + str(page)  # + '.html'

    def start_requests(self):
        try:
            for page in range(self.total_page):
                url = self.get_url(self.start_page + page)
                print('初始链接：', url)
                yield scrapy.Request(url)
        except Exception as e:
            print('初始链接出错：', e)

    def parse(self, response):
        try:
            xpath = '//*[@id="Search__content_left___2MajJ"]/div[9]/div/a/@href'
            links = response.xpath(xpath).extract()
            for link in links:
                link = response.urljoin(link)  # 补全链接地址
                print('第二层链接：', link)
                yield scrapy.Request(link, callback=self.parse_detail)
                # break  # 测试时使用
        except Exception as e:
            print('第1层解析中出错', e)
        pass

    def parse_detail(self, response):
        item = MagnetItem()
        try:
            item['filename'] = response.xpath('//h1[@class="res-title"]/text()')[0].extract()
            item['length'] = response.xpath('//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[3]/text()')[0].extract()
            item['ctime'] = response.xpath('//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[4]/text()')[0].extract()
            item['click'] = '未提供'
            item['link'] = response.xpath('//*[@id="Information__container___2meHB"]/div[2]/div[2]/a/@href')[0].extract()

            # 处理翻译
            message = re.findall('(.*?)\d', item['filename'])[0]  # 提取文件名中数字之前的英文字母
            message = ' '.join(message.split('.')).lower()  # 将.转换成空格，并小写
            # print(message)
            if message.endswith(' s'):  # 去掉以空格加s结尾的部分
                message = message[:-2]
            item['baidu'] = message
            api = 'http://fanyi.youdao.com/openapi.do' \
                  '?keyfrom=wufeifei&key=716426270&type=data&doctype=json&version=1.1&q='
            url = api + quote(message)  # quote的作用是屏蔽特殊的字符  urllib.parse.quote(text)
            # print(api)
            yield scrapy.Request(url=url, meta={'item': item}, callback=self.parse_fanyi)  #
        except Exception as e:
            print('第2层解析中出错：', e)

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
