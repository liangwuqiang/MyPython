import scrapy
from Demo.items import DemoItem
# from getkeyword import GetKeyword


class ExampleSpider(scrapy.Spider):
    name = 'example'
    # allowed_domains = ['example.com']
    # start_urls = ['http://example.com/']
    # start_urls = ['https://www.cnblogs.com/kongzhagen/p/6549053.html/']
    print('调试')

    def parse(self, response):  # <class 'scrapy.http.response.html.HtmlResponse'>
        css_title = '#cb_post_title_url::text'
        # css_content = '#cnblogs_post_body'
        css_content = '.blogpost-body'

        item = DemoItem()
        try:
            item['url'] = response.url
            item['title'] = response.css(css_title).extract_first()
            item['content'] = response.css(css_content).extract_first()

            item['image_urls'] = []
            image_urls = response.xpath('//img//@src').extract()
            for image_url in image_urls:
                if image_url.startswith('http') is False:
                    image_url = 'https:' + image_url
                item['image_urls'].append(image_url)

            # for i in item['image_urls']:
            #     print(i)
        except Exception as reason:
            print('程序出错: ', reason)

        yield item
