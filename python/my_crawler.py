import hashlib
from urllib import request
from bs4 import BeautifulSoup
import re
import os
import requests
import socket  # socket模块是针对 服务器端 和 客户端Socket 进行【打开】【读写】【关闭】
socket.setdefaulttimeout(30)  # 设置超时时间为30s


class MyCrawler(object):
    key_title = ""  # 提取标题的关键字
    key_content = ""  # 提取内容的关键字
    url = ""  # 当前的url
    urls = []  # 要进行提取的全部url
    html = ""  # 网页内容
    title = ""  # 提取到的标题
    content = ""  # 提取到的内容

    def __init__(self, urls):
        self.urls = urls.split()

    @classmethod
    def md5(cls, image_url):  # 将图片的url转换成哈希吗
        if not isinstance(image_url, str):
            image_url = str(image_url)
        md5 = hashlib.md5()
        md5.update(image_url.encode('utf-8'))
        return md5.hexdigest()

    def get_key_word(self):
        if 'jobbole.com' in self.url:  # 伯乐在线
            self.key_title = '.entry-header'
            self.key_content = '.entry'
        elif 'blog.csdn.net' in self.url:  # csdn
            # self.key_title = '.link_title'
            # self.key_content = '#article_content'
            self.key_title = '.title-article'
            self.key_content = '.htmledit_views'
        elif 'www.codingpy.com' in self.url:  # 编程派网址
            self.key_title = '.header h1'
            self.key_content = '.article-content'
        elif 'jingyan.baidu.com' in self.url:  # 百度经验
            self.key_title = '.exp-title h1'
            self.key_content = '.exp-article'
        elif 'www.cnblogs.com' in self.url:  # 博客园
            self.key_title = '.postTitle2'
            self.key_content = '.blogpost-body'
        elif 'www.jianshu.com' in self.url:  # 简书
            self.key_title = '.title'
            self.key_content = '.article'
        else:
            self.key_title = ''
            self.key_content = ''

    def get_html(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        req = request.Request(self.url, headers=headers)
        # req = request.Request(self.url)
        response = request.urlopen(req)
        self.html = response.read().decode('utf-8')
        # print(html)

    def get_content(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        self.title = soup.select(self.key_title)[0].text.strip()  # 文章标题
        print('文章标题：', self.title)
        self.content = soup.select(self.key_content)[0]  # 文章内容

    def get_images(self):
        content = str(self.content)
        pattern = '<img .*?src=\"(.*?)\"'  # .*? 后面多个问号，代表非贪婪模式，也就是说只匹配符合条件的最少字符
        re_image = re.compile(pattern)
        path = self.title + "_files/"
        for image_link in re_image.findall(content):
            if not os.path.exists(path):  # 创建图像存放目录
                os.mkdir(path)

            if "http" in image_link:  # 修正图片的url地址
                image_link_new = image_link
            else:
                image_link_new = "http:" + image_link
            print(image_link_new)

            filename = path + self.md5(image_link_new)
            ext_name = os.path.splitext(image_link_new)[-1]
            if ext_name == ".jpg" or ext_name == ".png":
                filename = filename + ext_name
            else:
                filename = filename + ".png"

            try:
                # request.urlretrieve(image_link_new, filename)
                res = requests.get(image_link_new)
                with open(filename, 'wb') as f:
                    f.write(res.content)
                print('下载完成 >>> ', filename)
            except Exception as e:
                print('图片出错', e)
            else:
                content = content.replace(image_link, filename)
        print('图片下载全部完成--------')

    def format_html(self):
        html_template = """<!DOCTYPE html>
        <html><head><meta charset="UTF-8">
        </head><body>
        <p><a href="{origin}">原文链接</a></p>
        <p><center><h1>{title}</h1></center></p>
            {content}
        </body></html>"""
        self.html = html_template.format(origin=self.url, title=self.title, content=self.content)

    def save_file(self):
        filename = self.title + ".html"
        with open(filename, "w", encoding='UTF-8') as f:
            f.write(self.html)
            # f.write(html.replace(u'\xa0', u' ').replace(u'\U0001f60a', u' '))

    def run(self):
        for url in self.urls:
            self.url = url
            self.get_key_word()
            if self.key_title == '' or self.key_content == '':
                return
            self.get_html()
            self.get_content()
            self.get_images()
            self.format_html()
            self.save_file()
            break


def main():
    # 现可提取的网站有：
    # 伯乐在线
    # csdn
    # 编程派网址
    # 百度经验
    # 博客园
    # 简书
    urls = """
    
http://python.jobbole.com/89091/

        """
    crawler = MyCrawler(urls)
    crawler.run()
    print("==运行结束==")


if __name__ == '__main__':
    main()
