# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MagnetItem(scrapy.Item):
    # define the fields for your item here like:
    # 西刺代理 https://www.bturl.cc/
    IP = scrapy.Field()  # ip地址
    PORT = scrapy.Field()  # 端口
    TYPE = scrapy.Field()  # 协议类型
    LOCATION = scrapy.Field()  # 地理位置
    SPEED = scrapy.Field()  # 速度
    LAST_CHECK_TIME = scrapy.Field()  # 最后验证时间
    # bt磁力链 https://www.bturl.cc/
    filename = scrapy.Field()  # 文件名
    length = scrapy.Field()  # 文件长度
    ctime = scrapy.Field()  # 创建时间
    click = scrapy.Field()  # 访问热度
    link = scrapy.Field()  # 磁力链接
    baidu = scrapy.Field()  # 百度搜索
    fanyi = scrapy.Field()  # 翻译
    # 其它 ===================
    pass
