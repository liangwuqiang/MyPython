import scrapy
from Demo.items import DemoItem
from Demo.Lib.getkeyword import GetKeyword


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']
    start_urls = [
        'https://scrapy-chs.readthedocs.io/zh_CN/0.24/topics/selectors.html',
        # 'https://blog.csdn.net/qq_19330913/article/details/80468494',  # 如何在Ubuntu 18.04上安装和使用PostgreSQL
    ]

    def parse(self, response):  # <class 'scrapy.http.response.html.HtmlResponse'>
        dict = GetKeyword().get_css_keyword(response.url)
        key_title = dict['title']
        key_content = dict['content']
        print('标题提取关键字： ', key_title)
        print('内容提取关键字： ', key_content)

        item = DemoItem()
        try:
            item['url'] = response.url
            item['title'] = response.css(key_title).extract_first()
            item['content'] = response.css(key_content).extract_first()
            print(item['title'])

            item['full_image_urls'] = []
            item['raw_image_urls'] = response.xpath('//img//@src').extract()
            if len(item['raw_image_urls']) != 0:
                for image_url in item['raw_image_urls']:
                    if image_url.startswith('http') is False:
                        # image_url = 'https:' + image_url
                        image_url = 'https://www.helplib.com' + image_url
                    item['full_image_urls'].append(image_url)
                # 调试
                for image_url in item['full_image_urls']:
                    print(image_url)
        except Exception as reason:
            print('程序出错: ', reason)

        yield item

