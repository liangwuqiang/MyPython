import hashlib
# 定义pipelines

# 别忘了在setting.py的ITEM_PIPELINES中添加你自己定义的pipeline
# 参考: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DemoPipeline(object):

    @classmethod
    def md5(cls, image_url):  # 这是我以前用的是.md5() 32位
        if not isinstance(image_url, str):
            image_url = str(image_url)
        md5 = hashlib.md5()
        md5.update(image_url.encode('utf-8'))
        return md5.hexdigest()

    @classmethod
    def sha1(cls, image_url):  # scrapy用的是.sha1() 40位
        if not isinstance(image_url, str):
            image_url = str(image_url)
        sha1 = hashlib.sha1()
        sha1.update(image_url.encode('utf-8'))
        return sha1.hexdigest()

    @classmethod
    def format_html(cls, url, title, content):
        html_template = """<!DOCTYPE html>
            <html><head><meta charset="UTF-8">
            </head><body>
            <p><a href="{origin}">原文链接</a></p>
            <p><center><h1>{title}</h1></center></p>
                {content}
            </body></html>"""
        html = html_template.format(origin=url, title=title, content=content)
        return html

    def process_item(self, item, spider):
        url = item['url']
        title = item['title']
        content = item['content']

        for image_url in item['image_urls']:
            content = content.replace(image_url, 'full/' + self.sha1(image_url) + '.jpg')

        html = self.format_html(url, title, content)
        filename = 'output/' + title + '.html'
        with open(filename, 'w') as f:
            f.write(html)
        # print(html)
        return item
