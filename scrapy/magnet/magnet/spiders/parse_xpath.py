import scrapy


class ParseXpathSpider(scrapy.Spider):
    name = 'parse_xpath'
    start_urls = [
        'file:///D:/PyProjects/scrapy/magnet/output/temp.html'
    ]

    def parse(self, response):
        print('起始链接：', response.url)
        print(response.text)
        print('=====分界线=====')
        try:
            # xpath = '//*[@id="Search__content_left___2MajJ"]/div[9]/div/a/@href'
            # links = response.xpath(xpath).extract()
            # for link in links:
                # print('第二层链接：', link)
            # =================================
            xpath = '//*[@id="Information__title___3V6H-"]/text()'
            title = response.xpath(xpath)[0].extract()
            print('标题：', title)

            xpath = '//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[4]/text()'
            # //*[@id="Information__container___2meHB"]/div[3]/div[2]/b[4]
            time = response.xpath(xpath)[0].extract()
            print('收录时间：', time)

            xpath = '//*[@id="Information__container___2meHB"]/div[3]/div[2]/b[3]/text()'
            # //*[@id="Information__container___2meHB"]/div[3]/div[2]/b[3]
            size = response.xpath(xpath)[0].extract()
            print('文件大小：', size)

            xpath = '//*[@id="Information__container___2meHB"]/div[2]/div[2]/a/@href'
            # //*[@id="Information__container___2meHB"]/div[2]/div[2]/a
            magnet = response.xpath(xpath)[0].extract()
            print('磁力链接：', magnet)
        except Exception as e:
            print('解析出现异常：', e)
