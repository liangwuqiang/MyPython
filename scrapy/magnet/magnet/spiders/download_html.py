import scrapy
import codecs


class DownloadHtmlSpider(scrapy.Spider):
    name = 'download_html'
    start_urls = [
        'https://www.cilimao.cc/information/2424415A59C9791C51DB996F6BAA6D24D89A001D?r=1090'
    ]

    def parse(self, response):
        try:
            print('起始链接：', response.url)
            html = response.text
            filename = 'output/temp.html'
            with codecs.open(filename, 'w', encoding='utf-8') as f:
                f.write(html)
        except Exception as e:
            print('出现异常：', e)
