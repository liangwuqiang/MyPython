"""
功能：   用于获取代理ip, 给其它爬虫使用
        获取的ip存放于ip.text中
"""

import scrapy
from magnet.items import MagnetItem


class BturlSpider(scrapy.Spider):
    name = 'xici'
    # allowed_domains = ['xicidaili.com']
    # start_urls = ['http://www.xicidaili.com/nn/']
    start_urls = ['file:///home/ubuntu/Documents/xici1.html',
                  'file:///home/ubuntu/Documents/xici2.html',
                  'file:///home/ubuntu/Documents/xici3.html',
                  ]
    with open('ip.txt', 'w') as f:
        f.write('')

    def parse(self, response):
        # items = []
        try:
            ip_list = response.xpath('//table[@id="ip_list"]/tbody')
            ips = ip_list[0].xpath('tr')
            for ip in ips[1:]:
                item = MagnetItem()
                tds = ip.xpath('td')
                ip_address = tds[1].xpath('text()')[0].extract()  # ip地址
                item['IP'] = ip_address
                port = tds[2].xpath('text()')[0].extract()  # 端口
                item['PORT'] = port
                location = tds[3].xpath('string(.)')[0].extract().strip()  # 地理位置
                item['LOCATION'] = location
                proxy_type = tds[5].xpath('text()')[0].extract()  # 协议类型
                item['TYPE'] = proxy_type
                speed = tds[6].xpath('div[@class="bar"]/@title').re('\d{0,2}\.\d{0,}')[0]  # 速度
                item['SPEED'] = speed
                check_time = tds[9].xpath('text()')[0].extract()  # 验证时间
                item['LAST_CHECK_TIME'] = check_time
                # items.append(item)
                yield item
        except Exception as e:
            print(e)
        print('完成')
        # return items
