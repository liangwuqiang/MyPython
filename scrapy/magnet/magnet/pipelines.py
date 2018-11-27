import codecs
from urllib.parse import quote
# -*- coding: utf-8 -*-

# 在这定义你的 item pipelines （也就是你要怎样处理传过来的item）

# 别忘了将你的 pipeline 添加到 setting 的 ITEM_PIPELINES 中 （在setting.py文件中开通ITEM_PIPELINES）
# 参考: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MagnetPipeline(object):
    items = []

    def process_item(self, item, spider):  # 程序运行过程中会不断调用这个
        print('==== MagnetPipeline.process_item ====')
        try:
            if spider.name == 'xici':  # 西刺代理单独输出，现在暂时不需要用
                print('爬取西刺代理ip：')
                with open('ip.txt', 'a') as f:
                    f.write(item['IP'] + ' ' + item['PORT'] + ' ' + item['TYPE'] + '\n')
                    print(item['IP'] + ' ' + item['PORT'] + ' ' + item['TYPE'] + '\n')
            else:
                self.items.append(item)
        except Exception as e:
            print('process_item 出错：', e)
        return item

    def close_spider(self, spider):  # 程序结束前会运行这个
        print('==== MagnetPipeline.close_spider ====')
        string_bulid = ''

        for item in self.items:
            # 构造各个项目
            filename = '<th><a href="' + item['link'] + '">' + item['filename'] + '</a></th>'
            ctime = '<td  align="center" valign="center">' + item['ctime'] + '</td>'
            length = '<td align="center" valign="center">' + item['length'] + '</td>'
            click = '<td align="center" valign="center">' + item['click'] + '</td>'
            link = 'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&' \
                   'tn=baidu&wd=' + quote(item['baidu']) + '&rsv_pq=db883fdf0000fbdb&' \
                   'rsv_t=d446v5MJbAY%2BN%2F7Q16VmFpuOR1uuuPAjHi0hyspbcfXe6pEO%2FnPi6DgO2xE&rqlang=cn&' \
                   'rsv_enter=1&rsv_sug3=3&rsv_sug1=3&rsv_sug7=100&rsv_sug2=0&inputT=1729&rsv_sug4=1729'
            fanyi = '<td align="center" valign="center"><a href="' + link + '">' + item['fanyi'] + '</td>'
            # 构造表格的一行，循环后变多行
            string_bulid = string_bulid + '<tr>' + filename + ctime + length + click + fanyi + '</tr>' + '\n'

        # 构造html模板，并填充数据
        html_template = """<!DOCTYPE html>
                <html><head><meta charset="UTF-8">
                </head><body>
                    <table style="border-collapse:collapse;" border="1">
                        <p style="text-align:center "><a href="https://www.bturl.cc/">BT磁力链</a></p>
                        <tr>
                          <th>文件名</th>
                          <td align="center" valign="center">创建日期</td>
                          <td align="center" valign="center">文件大小</td>
                          <td align="center" valign="center">下载热度</td>
                          <td align="center" valign="center">翻译&百度查询</td>
                        </tr>
                        {content}
                    </table>
                </body></html>"""
        html = html_template.format(content=string_bulid)

        # 输出到html文件中
        with codecs.open(spider.name + '.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print('程序运行完毕！！！')
