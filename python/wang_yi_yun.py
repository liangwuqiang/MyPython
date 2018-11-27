"""
这是一个在动态网页下抓取数据的一个例子
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import csv


class WangYiYun(object):
    url = ''

    def __init__(self, url):
        self.url = url

    def run(self):
        csv_file = open('playlist.csv', 'w', newline='')
        writer = csv.writer(csv_file)
        writer.writerow(['标题', '播放数', '链接'])

        i = 0
        url = self.url
        while url != 'javascript:void(0)':
            i = i+1
            print('调试', i)
            print(url)

            # 无界面调用‘火狐’浏览器的方法
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            driver = webdriver.Firefox(options=options)
            # print(help(webdriver.Firefox))  # 查看方法的配置信息

            driver.get(url)  # 全局的内容
            driver.switch_to.frame("contentFrame")  # 局部的内容
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            divs = soup.select('.u-cover.u-cover-1')

            for div in divs:
                nb = div.select('.nb')[0].text
                if '万' in nb and int(nb.split("万")[0]) > 500:
                    title = div.select('.msk')[0]['title']
                    link = 'https://music.163.com/#' + div.select('.msk')[0]['href']
                    # 样例 https://music.163.com/#/playlist?id=2065883262
                    print(title, nb, link)
                    writer.writerow([title, nb, link])

            url = 'https://music.163.com/#' + soup.select('a.zbtn.znxt')[0]['href']
        csv_file.close()


def main():
    start_url = 'https://music.163.com/#/discover/playlist'
    crawler = WangYiYun(start_url)
    crawler.run()
    print('完成')


if __name__ == '__main__':
    main()
