import scrapy
from Demo.items import DemoItem
from Demo.spiders.getkeyword import GetKeyword


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']
    start_urls = ['https://www.cnblogs.com/kongzhagen/p/6549053.html/']

    def parse(self, response):  # <class 'scrapy.http.response.html.HtmlResponse'>
        dict = GetKeyword().get_css_keyword(response.url)
        key_title = dict['title']
        key_content = dict['content']
        print(key_title)
        print(key_content)

        item = DemoItem()
        try:
            item['url'] = response.url
            item['title'] = response.css(key_title).extract_first()
            item['content'] = response.css(key_content).extract_first()

            item['image_urls'] = []
            image_urls = response.xpath('//img//@src').extract()
            for image_url in image_urls:
                if image_url.startswith('http') is False:
                    image_url = 'https:' + image_url
                item['image_urls'].append(image_url)
            # 调试
            for image_url in item['image_urls']:
                print(image_url)
        except Exception as reason:
            print('程序出错: ', reason)

        yield item
