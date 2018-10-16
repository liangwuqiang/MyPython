# -*- coding: utf-8 -*-

# Scrapy settings for Demo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Demo'

SPIDER_MODULES = ['Demo.spiders']
NEWSPIDER_MODULE = 'Demo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Demo (+http://www.yourdomain.com)'

# Obey robots.txt rules 遵守robots.txt的规则
# ROBOTSTXT_OBEY = True
ROBOTSTXT_OBEY = False  # 不遵守规则

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32  # 并发请求的个数 100

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3  # 下载延迟的时间
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False  # 禁用可以提高性能。但登录必须用

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False  # 与扩展功能相对应

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {  # 默认的请求头设置
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {  # 配置爬虫中间件
#    'Demo.middlewares.DemoSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {  # 配置下载中间件
#    'Demo.middlewares.DemoDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {  # 使用扩展功能
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {  # 项目管道设置
    'Demo.pipelines.DemoPipeline': 300,
    'scrapy.pipelines.images.ImagesPipeline': 1,
}
IMAGES_URLS_FIELD = 'full_image_urls'  # 指定图像链接的字段名，默认的字段名应该不用指定
IMAGES_STORE = r'./output'  # 指定图片输出的目录 还有一层full目录

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 指定输出log文件，这样运行时就不会显示log内容
LOG_FILE = "scrapy.log"  # 指定log文件名
