# 有待重新验证


class GetKeyword:
    def __init__(self):
        self.dict = {'title': '', 'content': ''}

    def get_css_keyword(self, url):
        if 'jobbole.com' in url:  # 伯乐在线
            self.dict['title'] = '.entry-header'
            self.dict['content'] = '.entry'
        elif 'blog.csdn.net' in url:  # csdn
            # key_title = '.link_title'
            # key_content = '#article_content'
            self.dict['title'] = '.title-article'
            # key_content = '.htmledit_views'
            self.dict['content'] = '.markdown_views.prism-dracula'
            # https://blog.csdn.net/weixin_36279318/article/details/79475388
            #dict['content'] = '.article_content.clearfix.csdn-tracking-statistics'
            # https://blog.csdn.net/qq_29186489/article/details/78661008

        elif 'www.codingpy.com' in url:  # 编程派网址
            self.dict['title'] = '.header h1'
            self.dict['content'] = '.article-content'
        elif 'jingyan.baidu.com' in url:  # 百度经验
            self.dict['title'] = '.exp-title h1'
            self.dict['content'] = '.exp-article'
        # elif 'www.cnblogs.com' in url:  # 博客园
        #     dict['title'] = '.postTitle2'
        #     dict['content'] = '.blogpost-body'
        elif 'www.jianshu.com' in url:  # 简书
            self.dict['title'] = '.title'
            self.dict['content'] = '.article'
        elif 'www.maiziedu.com' in url:  # 麦子学院
            self.dict['title'] = '.cont h1'
            self.dict['content'] = '.cont'
        elif 'www.cnblogs.com' in url:  # 博客园 ===============
            # https://www.cnblogs.com/kongzhagen/p/6549053.html/
            self.dict['title'] = '#cb_post_title_url::text'
            self.dict['content'] = '#cnblogs_post_body'
            # self.dict['content'] = '.blogpost-body'
        elif 'www.helplib.com' in url:  # 帮酷 ===============
            # https://www.helplib.com/linux/article_13528
            self.dict['title'] = '#article_subject a::text'
            self.dict['content'] = '#article_html_content'
        elif 'www.imooc.com' in url:  # 手记 ===============
            # https://www.imooc.com/article/21840
            self.dict['title'] = '.js-title::text'
            self.dict['content'] = '.detail-content'
        else:
            print('当前网页没能提取到关键字...')

        return self.dict
